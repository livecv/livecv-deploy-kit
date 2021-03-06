import sys,time
import os
import platform
import getopt
import json
import shutil
import argparse
import requests as re
import urllib.parse
import zipfile
from livepm.lib.command import Command
from livepm.lib.configuration import Configuration

server_url = "https://livekeys.io/api"

class InstallCommand(Command):

    name = 'install'
    description = 'Install a live package'

    def __init__(self):
        pass

    def parse_args(self, argv):
        parser = argparse.ArgumentParser(description='Install a live package')
        parser.add_argument('name', default=None, nargs='?', help='Name of the package')
        parser.add_argument('--server_url', '-sU', default=server_url, help='Change server url.')
        parser.add_argument('--install_globally', '-g' ,default=False, action='store_true', help="Install to livekeys dir")

        args = parser.parse_args(argv)

        self.name   = args.name
        self.release   = ''
        self.server_url   = args.server_url
        self.current_version = ''
        
        # Directory construction
        if args.install_globally:
            
            try:
                if os.environ['LIVEKEYS_DIR']:
                    self.dir = os.environ["LIVEKEYS_DIR"]
                    self.folder = 'plugins'

            except KeyError:
                print("Enviroment variable LIVEKEYS_DIR not set.")
                sys.exit(1)

        else:
            self.dir = os.getcwd()
            self.folder = 'packages'
    
    def __call__(self):

        # Get the os for release extension
        if platform.system() == 'Linux':
            self.release = 'linux'

        elif platform.system() == 'Darwin':

            self.release = 'macos'

        elif platform.system() == 'Windows':

            self.release = 'win'

        # Check url here
        try:

            r = re.get(self.server_url)

        except:
            
            print('Invalid url.')
            sys.exit(1)


        # progress bar
        def update_progress(title, progress):
            length = 40
            block = int(round(length*progress))
            msg = "\r{0}: [{1}] {2}%".format(title, "#"*block + "-"*(length-block), round(progress*100, 2))
            if progress >=1: 
                msg += "DONE\r\n"
            sys.stdout.write(msg)
            sys.stdout.flush()

        # Dependency download
        def downloadDependencies(versions):

            for i in versions:
                
                version = i['version']
                packageName = i['package']['name']
                dependencyUrl = i['url']
                dependencyPath = os.path.join(os.path.join(plugin_directory, self.name + '-' + self.current_version[:-4]), packageName + '-' + version[:-4])                
                package = {packageName:version}
                
                if os.path.exists(os.path.join(os.path.join(plugin_directory, self.name + '-' + self.current_version[:-4]), 'live.package.json')):
                    
                    # Read from file if exists
                    with open(os.path.join(os.path.join(plugin_directory, self.name + '-' + self.current_version[:-4]), 'live.package.json')) as livePackages:
                        data = json.load(livePackages)
                        current = data['dependencies']
                        current.update(package)

                        # Write updated data
                        with open(os.path.join(os.path.join(plugin_directory, self.name + '-' + self.current_version[:-4]), 'live.package.json'), "w") as livePackages:
                            
                            json.dump(data, livePackages,ensure_ascii=False, indent=4)
                            
                else:
                    # Create live.package.json and write default data
                    with open(os.path.join(os.path.join(plugin_directory, self.name + '-' + self.current_version[:-4]),"live.package.json"), 'w') as livePackages:
                        
                        package_details = {
                            
                            "name": self.name, 
                            "version": self.current_version[:-4],
                            "dependencies": package
                            }
                        json.dump(package_details, livePackages,ensure_ascii=False, indent=4)

                # Download dependency
                open( dependencyPath + '.zip' , 'wb').write(getZip.content)
                # unzip main package and remove zip file
                zipPath = (dependencyPath + '.zip')
                zip = zipfile.ZipFile(zipPath)
                zip.extractall(dependencyPath)
                zip.close()
                os.remove(dependencyPath + '.zip')
                downloadDependencies(i['dependencies'])

        # Install from json list here
        if not self.name:

            if os.path.exists(os.path.join(os.getcwd(), 'live.package.json')):
                # read json
                with open(os.path.join(os.getcwd(),"live.package.json")) as livePackages:
                    data = json.load(livePackages)
                
                    for package, version in data['dependencies'].items():

                        urlParams = 'package/' + package + '/release/' + version + '/' + self.release
                        url = urllib.parse.urljoin(self.server_url, urlParams)
                        r = re.get(url, allow_redirects=True)
                        self.name = package

                        if r.ok:

                            data = r.text
                            resp = json.loads(data)

                            # current package dependencies
                            dependencies = resp['dependencies']

                            # Package installation progress bar
                            num_of_packages = []
                            # Append id's of packages for package count
                            num_of_packages.append(resp['package'])
                            # # use number of packages for iteration
                            for i in range(len(num_of_packages)):
                                update_progress("installing " + package, i/len(num_of_packages))

                            # Finished
                            update_progress("Installing " + package, 1)

                            # Request the zip file
                            getZip = re.get(resp['url'])
                            
                            # # install main packages
                            plugin_directory= os.path.join(self.dir, self.folder)

                            if not os.path.exists(plugin_directory):
                                
                                os.makedirs(plugin_directory)

                            else:
                                pass

                            package_path = os.path.join(plugin_directory, package + '-' + version[:-4])
                            
                            if os.path.exists(package_path):
                                print('Package: ' + package + ' ' + version + ' already installed')

                            else:

                                open( package_path + '.zip', 'wb').write(getZip.content)

                                # # unzip main package and remove zip file
                                zipPath = (package_path + '.zip')
                                zip = zipfile.ZipFile(zipPath)
                                zip.extractall(package_path)
                                zip.close()
                                os.remove(package_path + '.zip')

                                self.current_version = resp['version']
                                package = {self.name:self.current_version}

                                downloadDependencies(dependencies)

                                for i in resp['dependencies']:
                                    progressBarLen = i['dependencies']

                                    for i in range(len(progressBarLen)):
                                        update_progress("installing dependencies:", i/len(progressBarLen))
                                    # # Finished
                                    update_progress("Installing dependencies:" , 1)
                            
                        # Note if the package is not found
                        else:
                            print('Package ' + package + ' not found.')

            # live.package.json missing
            else:

                print('live.package.json not found.')
                sys.exit(1)
        else:

            # Construct url
            urlParams = 'package/' + self.name + '/' + 'latest/' + self.release
            url = urllib.parse.urljoin(self.server_url, urlParams)
            # Send request
            r = re.get(url, allow_redirects=True)            
            # Check the url
            if r.ok:
                
                # change var names
                resp = json.loads(r.text)

                # Check if the package.lock exist and create one if not
                if not os.path.exists(os.path.join(os.getcwd(), 'live.package.lock')):
                    open(os.path.join(os.getcwd(), 'live.package.lock'),'w')

                else:
                    print('Already running!')
                    sys.exit(1)

                # Package path construction
                plugin_directory= os.path.join(self.dir, self.folder)
                
                # Create folder if installing in cwd
                if os.environ != ["LIVEKEYS_DIR"]:

                    # Check if the package is installed
                    try:
                        os.makedirs(os.path.join(plugin_directory, self.name + '-' + resp['version'][:-4]))

                    except:
                        print('Package ' + self.name + ' already installed.')
                        # remove package.lock
                        os.remove(os.path.join(os.getcwd(), 'live.package.lock'))
                        sys.exit(1)

                jsonResponse = json.loads(r.text)
                
                # Request the zip file
                getZip = re.get(jsonResponse['url'])
                
                # Read dependencies
                versions = jsonResponse['dependencies']

                # Package installation progress bar
                num_of_packages = []
                # Append id's of packages for package count
                num_of_packages.append(jsonResponse['package'])
                # # use number of packages for iteration
                for i in range(len(num_of_packages)):
                    update_progress("installing " + self.name, i/len(num_of_packages))

                # Finished
                update_progress("Installing " + self.name, 1)

                # install main packages
                package_path = os.path.join(plugin_directory, self.name + '-' + jsonResponse['version'][:-4])
                open( package_path + '.zip', 'wb').write(getZip.content)

                # unzip main package and remove zip file
                zipPath = (package_path + '.zip')
                zip = zipfile.ZipFile(zipPath)
                zip.extractall(package_path)
                zip.close()
                os.remove(package_path + '.zip')
                # Create live.package.json for project
                self.current_version = jsonResponse['version']
                package = {self.name:self.current_version}
                if os.path.exists(os.path.join(os.getcwd(), 'live.package.json')):
                    
                    # Read live.package.json
                    with open(os.path.join(os.getcwd(),"live.package.json")) as livePackages:
                        data = json.load(livePackages)
                        current = data['dependencies']
                        current.update(package)

                    # Write updated data
                    with open(os.path.join(os.getcwd(),"live.package.json"), "w") as livePackages:
                        
                        json.dump(data, livePackages,ensure_ascii=False, indent=4)

                else:
                    # Create live.package.json and write default data
                    with open(os.path.join(os.getcwd(),"live.package.json"), 'w') as livePackages:
                        package_details = {
                            
                            "name": os.path.basename(os.getcwd()), 
                            "version": '0.1.0',
                            "dependencies": package

                            }
                        json.dump(package_details, livePackages,ensure_ascii=False, indent=4)
                
                downloadDependencies(versions)

                for i in jsonResponse['dependencies']:
                    
                    progressBarLen = i['dependencies']

                    for i in range(len(progressBarLen)):
                        update_progress("installing dependencies for " + self.name, i/len(progressBarLen))
                    # # Finished
                    update_progress("Installing dependencies for " + self.name, 1)

                # remove package.lock
                os.remove(os.path.join(os.getcwd(), 'live.package.lock'))

            else:

                print("Package not found")
