"""This is a modified version of snapcraft's autotools plugin.

It calls erlang's otp_build script before configure.
"""

import snapcraft


class AutotoolsPlugin(snapcraft.BasePlugin):

    @classmethod
    def schema(cls):
        schema = super().schema()
        schema['properties']['configflags'] = {
            'type': 'array',
            'minitems': 1,
            'uniqueItems': True,
            'items': {
                'type': 'string',
            },
            'default': [],
        }

        # Inform Snapcraft of the properties associated with building. If these
        # change in the YAML Snapcraft will consider the build step dirty.
        schema['build-properties'].extend(['configflags'])

        return schema

    def __init__(self, name, options, project):
        super().__init__(name, options, project)
        self.build_packages.extend([
            'autoconf',
            'make',
        ])

    def build(self):
        super().build()
        self.run(['./otp_build', 'autoconf'])

        self.run(['./configure'] + self.options.configflags)
        self.run(['make', '-j{}'.format(self.parallel_build_count)])
        self.run(['make', 'install', 'DESTDIR=' + self.installdir])
