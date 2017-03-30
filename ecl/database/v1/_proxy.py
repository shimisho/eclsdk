# Licensed under the Apache License, Version 2.0 (the "License"); you may
# not use this file except in compliance with the License. You may obtain
# a copy of the License at
#
#      http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS, WITHOUT
# WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied. See the
# License for the specific language governing permissions and limitations
# under the License.

from ecl.database.v1 import instance as _instance
from ecl.database.v1 import user as _user
from ecl.database.v1 import database as _database
from ecl.database.v1 import flavor as _flavor

from ecl import proxy2
from ecl import resource2


class Proxy(proxy2.BaseProxy):

    def instances(self, **query):
        """Retrieve a list of instances

        :param kwargs \*\*query: Optional query parameters to be sent to limit
                                 the instances being returned.
        :returns: A list of database instances.
        """
        instance = _instance.Instance
        return list(self._list(instance, paginated=False, **query))

    def create_instance(self,
                        name,
                        flavor_id,
                        volume,
                        databases,
                        users,
                        datastores,
                        nics,
                        availability_zone=None,
                        backup_window=None,
                        backup_retension_period=None,
                        maintenance_window=None,
                        **attrs):
        """Create a new instance from attributes

        :param string name: Name of instance
        :param string flavor_id: Flavor ID of server
        :param dict volue: Volume configuration dict which has volume_size inside
        :param databases: Database definition
                list to initialize database on creating instance
        :param users: List of users to connect to defined databases
        :param dict datastores: Datastore name and version of instance
        :param dict nics: Network difinition of instance
        :param availability_zone: Availability zone for instance
        :param backup_window: Backup window time range
        :param backup_retension_period: Number of the day to retain backup
        :param maintenance_window: Maintenance window time range by
                the day of the week and from/to time
        :param kwargs attrs: Keyword arguments which will be used to create
                             a :class:`~ecl.datagase.v1.instance.Instance`,
                             comprised of the properties on the Instance class.

        :returns: The results of instance creation
        :rtype: :class:`~ecl.compute.v1.instance.Instance`
        """
        attrs.update({"name": name})
        attrs.update({"flavorRef": flavor_id})
        attrs.update({"volume": volume})
        attrs.update({"databases": databases})
        attrs.update({"users": users})
        attrs.update({"datastores": datastores})
        attrs.update({"nics": nics})

        if availability_zone:
            attrs.update({"availability_zone": availability_zone})
        if backup_window:
            attrs.update({"backup_window": backup_window})
        if backup_retension_period:
            attrs.update({"backup_retension_period": backup_retension_period})
        if maintenance_window:
            attrs.update({"maintenance_window": maintenance_window})

        return self._create(_instance.Instance, **attrs)

    def delete_instance(self, instance, ignore_missing=True):
        """Delete a instance

        :param instance: The value can be either the ID of a server or a
                         :class:`~ecl.database.v1.instance.Instance` instance.
        :param bool ignore_missing: When set to ``False``
                    :class:`~ecl.exceptions.ResourceNotFound` will be
                    raised when the server does not exist.
                    When set to ``True``, no exception will be set when
                    attempting to delete a nonexistent instance
        :param bool force: When set to ``True``, the instance deletion will be
                           forced immediatly.

        :returns: ``None``
        """
        self._delete(_instance.Instance, instance, ignore_missing=ignore_missing)

    def find_instance(self, name_or_id, ignore_missing=True):
        """Find a single instance

        :param name_or_id: The name or ID of a server.
        :param bool ignore_missing: When set to ``False``
                    :class:`~ecl.exceptions.ResourceNotFound` will be
                    raised when the resource does not exist.
                    When set to ``True``, None will be returned when
                    attempting to find a nonexistent resource.
        :returns: One :class:`~ecl.database.v1.instance.Instance` or None
        """
        return self._find(_instance.Instance, name_or_id,
                          ignore_missing=ignore_missing)

    def get_instance(self, instance):
        """Get a single instance

        :param instance: The value can be the ID of a instance or a
                       :class:`~ecl.database.v1.instance.Instance` instance.

        :returns: One :class:`~ecl.database.v1.instance.Instance`
        :raises: :class:`~ecl.exceptions.ResourceNotFound`
                 when no resource can be found.
        """
        return self._get(_instance.Instance, instance)

    def wait_for_server(self, instance, status='ACTIVE', failures=['ERROR'],
                        interval=2, wait=120):
        return resource2.wait_for_status(self.session, instance, status,
                                         failures, interval, wait)

    def find_flavor(self, name_or_id, ignore_missing=True):
        """Find a single flavor

        :param name_or_id: The name or ID of a flavor.
        :param bool ignore_missing: When set to ``False``
                    :class:`~ecl.exceptions.ResourceNotFound` will be
                    raised when the resource does not exist.
                    When set to ``True``, None will be returned when
                    attempting to find a nonexistent resource.
        :returns: One :class:`~ecl.database.v1.flavor.Flavor` or None
        """
        return self._find(_flavor.Flavor, name_or_id,
                          ignore_missing=ignore_missing)

    def get_flavor(self, flavor):
        """Get a single flavor

        :param flavor: The value can be the ID of a flavor or a
                       :class:`~ecl.database.v1.flavor.Flavor` instance.

        :returns: One :class:`~ecl.database.v1.flavor.Flavor`
        :raises: :class:`~ecl.exceptions.ResourceNotFound`
                 when no resource can be found.
        """
        return self._get(_flavor.Flavor, flavor)

    def flavors(self):
        """Return a list of flavors
        :returns: A list of flavor objects
        """
        return list(self._list(_flavor.Flavor, paginated=False))

    def users(self, instance_id, **query):
        """Retrieve a list of users assciated with instance

        :param instance_di: Instance id to find users
        :param kwargs \*\*query: Optional query parameters to be sent to limit
            the instances being returned.  Available parameters include:
        :returns: A list of database instances.
        """
        user = _user.User
        return list(self._list(user, paginated=False, instance_id=instance_id, **query))

    def create_user(self, instance_id, name, password, databases=None):
        """Create a new user from attributes

        :param string instance_id: ID of instance to assciate creating user
        :param string name: Name of user
        :param string password: Password of user
        :param databases: Database list of user to grant

        :returns: The results of user creation
        :rtype: :class:`~ecl.compute.v1.user.User`
        """
        attrs = {"name": name,
                 "password": password}
        if databases:
            attrs.update({"databases": databases})
        return self._create(_user.User, instance_id=instance_id, **attrs)

    def delete_user(self, instance_id, user, ignore_missing=True):
        """Delete a user

        :param instance_id: The value can be either the ID of a server or a
                           :class:`~ecl.database.v1.instance.Instance` instance.
        :param bool ignore_missing: When set to ``False``
                    :class:`~ecl.exceptions.ResourceNotFound` will be
                    raised when the resource does not exist.
                    When set to ``True``, no exception will be set when
                    attempting to delete a nonexistent user

        :returns: ``None``
        """
        self._delete(_user.User, user, instance_id=instance_id,
                     ignore_missing=ignore_missing)

    def find_user(self, instance_id, name_or_id, ignore_missing=True):
        """Find a single user

        :param name_or_id: The name or ID of a user.
        :param bool ignore_missing: When set to ``False``
                    :class:`~ecl.exceptions.ResourceNotFound` will be
                    raised when the resource does not exist.
                    When set to ``True``, None will be returned when
                    attempting to find a nonexistent resource.
        :returns: One :class:`~ecl.database.v1.user.User` or None
        """
        return self._find(_user.User, name_or_id,
                          instance_id=instance_id,
                          ignore_missing=ignore_missing)

    def databases(self, instance_id, **query):
        """Retrieve a list of databases assciated with instance

        :param instance_id: Instance id to find databases
        :param kwargs \*\*query: Optional query parameters to be sent to limit
            the instances being returned.  Available parameters include:
        :returns: A list of database instances.
        """
        database = _database.Database
        return list(self._list(database, paginated=False,
                               instance_id=instance_id, **query))

    def create_database(self, instance_id, name):
        """Create a new database from attributes

        :param string instance_id: ID of instance to assciate creating database
        :param string name: Name of database

        :returns: The results of database creation
        :rtype: :class:`~ecl.compute.v1.database.Database`
        """
        attrs = {"name": name}
        return self._create(_database.Database, instance_id=instance_id,
                            **attrs)

    def delete_database(self, instance_id, database, ignore_missing=True):
        """Delete a database

        :param instance_id: The value can be either the ID of a server or a
                           :class:`~ecl.database.v1.instance.Instance` instance.
        :param bool ignore_missing: When set to ``False``
                    :class:`~ecl.exceptions.ResourceNotFound` will be
                    raised when the resource does not exist.
                    When set to ``True``, no exception will be set when
                    attempting to delete a nonexistent database

        :returns: ``None``
        """
        self._delete(_database.Database, database, instance_id=instance_id,
                     ignore_missing=ignore_missing)

    def find_database(self, instance_id, name_or_id, ignore_missing=True):
        """Find a single database

        :param name_or_id: The name or ID of a database.
        :param bool ignore_missing: When set to ``False``
                    :class:`~ecl.exceptions.ResourceNotFound` will be
                    raised when the resource does not exist.
                    When set to ``True``, None will be returned when
                    attempting to find a nonexistent resource.
        :returns: One :class:`~ecl.database.v1.database.Database` or None
        """
        return self._find(_database.Database, name_or_id,
                          instance_id=instance_id,
                          ignore_missing=ignore_missing)
