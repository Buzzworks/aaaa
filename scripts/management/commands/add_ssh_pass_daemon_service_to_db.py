from django.core.management.base import BaseCommand
from callcenter.models import Daemons
from django.conf import settings
import platform
import getpass
import numpy as np
import os


class Command(BaseCommand):

    help = "Insert Default Daemon Services to DB"

    def handle(self, **options):
        primarySetup = input("Are you want to do primary setup?[y/n]")
        if primarySetup.lower() == "no" or primarySetup.lower() == "n":
            sshPwd = input(
                "Are you want to Create/Update the SSH Password?[y/n]")
            daemon_setup = "n"
        elif primarySetup.lower() == "yes" or primarySetup.lower() == "y":
            sshPwd = "y"
            daemon_setup = "y"
        else:
            self.stderr.write(
                "Entered Wrong Selection")
        if sshPwd.lower() == "yes" or sshPwd.lower() == "y":
            sshpassword_field = None
            while sshpassword_field is None:
                password = getpass.getpass("Enter SSH root Password")
                password2 = getpass.getpass('Password (again): ')
                if password != password2:
                    self.stderr.write(
                        "Error: Your passwords didn't match.")
                    # Don't validate passwords that don't match.
                    continue
                else:
                    sshpassword_field = [password]
            cwd = os.path.join(settings.BASE_DIR, 'static/')
            np.save('{}.sshpassword.npy'.format(cwd), np.char.encode(
                sshpassword_field, encoding='cp037'))
        if daemon_setup != "y":
            daemon_setup = input(
                "Are you want to add defalut service names?[y/n]")
        if daemon_setup.lower() == 'y' or daemon_setup.lower == 'yes':
            Daemons.objects.all().delete()
            os_type = platform.linux_distribution()
            if "Ubuntu" in os_type:
                webserver = 'apache2'
            else:
                webserver = 'httpd'
            Daemons.objects.bulk_create(
                [Daemons(service_name="freeswitch", status=True), Daemons(service_name="flexydial-cdrd", status=True), Daemons(service_name="flexydial-autodial", status=True), Daemons(service_name="flexydial-fs-dialplan", status=True), Daemons(service_name="postgresql", status=True), Daemons(service_name="redis", status=True), Daemons(service_name="postgresql", status=True), Daemons(service_name=webserver, status=True)])
            print("*********************************************************")
            print("!!!!!!!!!!  Daemons DATA CREATED SUCCEFULLY  !!!!!!!!!!")
            print("*********************************************************")
