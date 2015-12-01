import logging
import ssl

import ldap3
import ldap3.utils.dn

from . import utils

logger = logging.getLogger(__name__)

class LDAPServer:
    """This is a utilityclass for wrapping the raw LDAP operations into a nice api"""

    def __init__(self,
                 ldap_server_url="ldaps://sesam-ci-dc.cloudapp.net",
                 ldap_user="sesam-ci\\sesam",
                 ldap_password="BouvetSesam1234",
                 default_organizational_unit=None):

        self._ldap_server_url = ldap_server_url
        self._ldap_user = ldap_user
        self._ldap_password = ldap_password
        self._default_organizational_unit = default_organizational_unit

        self._tls = ldap3.Tls(
            validate=ssl.CERT_NONE,  # The server only has a self-signed certificate, so ignore it.
            # validate=ssl.CERT_REQUIRED # This is the setting we would have used in a production setting.
            )
        if self._ldap_server_url.startswith("ldaps"):
            self._ldap_server = ldap3.Server(self._ldap_server_url, use_ssl=True, tls=self._tls)
        else:
            self._ldap_server = ldap3.Server(self._ldap_server_url, use_ssl=False)

        self._test_user_password = "Testing123."
        self._user_object_classes = ['top', 'person', 'organizationalPerson', 'user']
        self._user_main_object_class = "organizationalPerson"

        self._organizational_unit_object_classes = ['top', 'organizationalUnit']
        self._organizational_unit_main_object_class = 'organizationalUnit'

    def __enter__(self):
        return self

    def __exit__(self, *exs):
        # This is currently a no-op, since we don't keep a connection open.
        return False

    def get_user_email_addresses(self, organizational_unit=None):
        """Returns a list with the emailaddresses of all the users in the specified organizational unit"""
        if organizational_unit is None:
            organizational_unit = self._default_organizational_unit

        emails = []
        for user in self.get_users(organizational_unit=organizational_unit, attributes=["mail"]):
            attributes = user['attributes']
            if "mail" in attributes:
                emails.append(attributes["mail"][0])
        return emails

    def get_users(self, organizational_unit=None,
                  attributes=ldap3.ALL_ATTRIBUTES):
        """Returns a list of all the users"""
        if organizational_unit is None:
            organizational_unit = self._default_organizational_unit

        search_base = self._get_searchbase(organizational_unit)
        search_filter = self._get_searchfilter()
        with self._create_connection() as ldap_connection:
            return ldap_connection.extend.standard.paged_search(search_base,
                                                                search_filter,
                                                                attributes=attributes,
                                                                paged_size=1000, generator=False)

    def get_user(self, given_name, family_name, organizational_unit=None, attributes=ldap3.ALL_ATTRIBUTES):
        if organizational_unit is None:
            organizational_unit = self._default_organizational_unit
        search_base = self._get_searchbase(organizational_unit)
        cn = self.get_user_cn(given_name, family_name)
        search_filter = "(& %s (cn=%s))" % (self._get_searchfilter(), cn,)
        with self._create_connection() as ldap_connection:
            users = ldap_connection.extend.standard.paged_search(search_base,
                                                                 search_filter,
                                                                 attributes=attributes,
                                                                 paged_size=10, generator=False)
            if len(users) > 1:
                raise AssertionError("Found %d users! There should be just one!" % (len(users),))
            if not users:
                raise AssertionError("The user '%s' was not found!" % (cn,))
            return users[0]

    def get_organizational_units(self, attributes=ldap3.ALL_ATTRIBUTES):
        """Returns a list of all the organizational units"""
        search_base = self._get_searchbase_for_organizational_unit()
        search_filter = self._get_searchfilter_for_organizational_unit()
        with self._create_connection() as ldap_connection:
            return ldap_connection.extend.standard.paged_search(search_base,
                                                                search_filter,
                                                                attributes=attributes,
                                                                paged_size=1000, generator=False)

    def add_organizational_unit(self, organizational_unit):
        with self._create_connection() as ldap_connection:
            dn = self.get_organizational_unit_dn(organizational_unit)

            display_name = organizational_unit

            attributes = dict(
                objectClass=self._organizational_unit_object_classes,
                displayName=display_name,
                name=organizational_unit,
            )
            success = ldap_connection.add(dn, attributes=attributes)
            if not success:
                raise AssertionError("Failed to add the organizational unit dn='%s'! ldap_connection.result:%s" % (
                    dn, ldap_connection.result))

            logger.info("Added the organizational unit dn='%s'. ldap_connection.result:%s" % (
                        dn, ldap_connection.result))

    def delete_organizational_unit(self, organizational_unit):
        with self._create_connection() as ldap_connection:
            dn = self.get_organizational_unit_dn(organizational_unit)
            success = ldap_connection.delete(dn)
            if not success:
                raise AssertionError("Failed to delete the organizational unit dn='%s'! ldap_connection.result:%s" % (
                    dn, ldap_connection.result))
            logger.info("Deleted the organizational unit dn='%s'. ldap_connection.result:%s" % (
                    dn, ldap_connection.result))

    def add_user(self, given_name, family_name,
                 username=None,  # If this is None, it will be generated from the given_name and family_name
                 email_address=None,  # If this is None, it will be set to "<username> + @sesam-ci.local".
                 organizational_unit=None,
                 attributes=None,
                 ):
        if username is None:
            username = utils.get_testuser_username(given_name, family_name)

        if email_address is None:
            email_address = username + "@sesam-ci.local"

        if organizational_unit is None:
            organizational_unit = self._default_organizational_unit

        with self._create_connection() as ldap_connection:
            dn = self.get_user_dn(given_name, family_name, organizational_unit)

            display_name = given_name + " " + family_name

            #unicode_pass = '\"' + self._test_user_password + '\"'
            unicode_pass =  self._test_user_password
            password_value = unicode_pass.encode('utf-16-le')

            combined_attributes = dict(
                #userAccountControl='514',  # Disabled until we set the password
                #userAccountControl='512',
                #unicodePwd=password_value,

                objectClass=self._user_object_classes,
                displayName=display_name,
                givenName=given_name,
                sAMAccountName=username,
                proxyAddresses="SMTP:" + username + "@sesam-ci.local",
                targetaddress="SMTP:" + username + "@sesam-ci.local",
                mail=email_address,
                mailNickname=username,
                userPrincipalName=email_address,
            )
            if family_name:
                combined_attributes["sn"] = family_name

            if not attributes is None:
                combined_attributes.update(attributes)

            success = ldap_connection.add(dn, attributes=combined_attributes)
            if not success:
                raise AssertionError("Failed to add the user dn='%s'! ldap_connection.result:%s" % (
                    dn, ldap_connection.result))

            if False:
                # Set the password and enable the account.
                changes = {'unicodePwd': [(ldap3.MODIFY_REPLACE, [password_value])],
                           'userAccountControl': [(ldap3.MODIFY_REPLACE, ['512'])]  # 512 will set user account to enabled
                           }
                success = ldap_connection.modify(dn, changes=changes)
                if not success:
                    raise AssertionError(
                        "Failed to set the password and enable the account for user dn='%s'! ldap_connection.result:%s" % (
                            dn, ldap_connection.result))

                # Create the ms exchange mailbox
                changes = dict(
                    )
                success = ldap_connection.modify(dn, changes=changes)
                if not success:
                    raise AssertionError(
                        "Failed to set the exchange attributes for the user dn='%s'! ldap_connection.result:%s" % (
                            dn, ldap_connection.result))

            logger.info("Added the user dn='%s'. ldap_connection.result:%s" % (
                        dn, ldap_connection.result))

    def delete_user(self, given_name, family_name, organizational_unit=None):
        if organizational_unit is None:
            organizational_unit = self._default_organizational_unit
        with self._create_connection() as ldap_connection:
            dn = self.get_user_dn(given_name, family_name, organizational_unit)
            success = ldap_connection.delete(dn)
            if not success:
                raise AssertionError("Failed to delete the user dn='%s'! ldap_connection.result:%s" % (
                    dn, ldap_connection.result))
            logger.info("Deleted the user dn='%s'. ldap_connection.result:%s" % (
                    dn, ldap_connection.result))

    def modify_user(self, given_name, family_name, changes,
                    organizational_unit=None):
        if organizational_unit is None:
            organizational_unit = self._default_organizational_unit
        with self._create_connection() as ldap_connection:
            dn = self.get_user_dn(given_name, family_name, organizational_unit)
            success = ldap_connection.modify(dn, changes)
            if not success:
                raise AssertionError("Failed to modify the user dn='%s'! ldap_connection.result:%s" % (
                    dn, ldap_connection.result))
            logger.info("Modified the user dn='%s'. ldap_connection.result:%s" % (
                    dn, ldap_connection.result))

    def get_user_cn(self, given_name, family_name):
        fullname = given_name + " " + family_name
        fullname = fullname.strip()
        cn = ldap3.utils.dn.escape_attribute_value(fullname)
        return cn

    def get_user_dn(self, given_name, family_name, organizational_unit):
        cn = self.get_user_cn(given_name, family_name)
        dn = "CN=" + cn + "," + self._get_searchbase(organizational_unit)
        return dn

    def get_organizational_unit_dn(self, organizational_unit):
        dn = """OU="%s",%s""" % (organizational_unit, self._get_searchbase_for_organizational_unit())
        return dn

    def _get_searchbase(self, organizational_unit):
        return """OU="%s",%s""" % (organizational_unit, self._get_searchbase_for_organizational_unit())

    @staticmethod
    def _get_searchbase_for_organizational_unit():
        return """DC=Sesam-CI,DC=local"""

    def _get_searchfilter_for_organizational_unit(self):
        return "(objectClass=%s)" % (self._organizational_unit_main_object_class,)

    def _get_searchfilter(self):
        return "(objectClass=%s)" % (self._user_main_object_class,)

    def _create_connection(self):
        """Utilitymethod used to ensure that we create the connections the same way everywhere."""
        return ldap3.Connection(self._ldap_server, user=self._ldap_user, password=self._ldap_password)
