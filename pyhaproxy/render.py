#!/usr/bin/env python
# -*- coding: utf-8 -*-


class Render(object):
    """Do rendering the config.Config object to a str

    Attributes:
        configuration (config.Configuration):
    """
    def __init__(self, configuration):
        self.configuration = configuration

    def render_configuration(self):
        # render global section
        config_str = self.render_global(self.configuration.globall)
        # render defaults sections
        for defaults_section in self.configuration.defaults:
            config_str = config_str + self.render_defaults(defaults_section)
        # render listen sections
        for listen_section in self.configuration.listens:
            config_str = config_str + self.render_listen(listen_section)
        # render frontend sections
        for frontend_section in self.configuration.frontends:
            config_str = config_str + self.render_frontend(frontend_section)
        # render backend sections
        for backend_section in self.configuration.backends:
            config_str = config_str + self.render_backend(backend_section)

        return config_str

    def dumps_to(self, filepath):
        with open(filepath, 'w') as f:
            f.write(self.render_configuration())
        print 'write configs into %s succeed' % filepath

    def render_global(self, globall):
        globall_str = '''
global

%s
        '''
        return globall_str % self.__render_config_block(
            globall.config_block)

    def render_defaults(self, defaults):
        defaults_str = '''
defaults %s

%s
        '''
        return defaults_str % (defaults.name, self.__render_config_block(
            defaults.config_block))

    def render_userlist(self, userlist):
        return ''

    def render_listen(self, listen):
        listen_str = '''
listen %s %s

%s
        '''
        host_port = ''
        if not bool(listen.config_block['binds']):
            host_port = '%s:%s' % (listen.host, listen.port)

        return listen_str % (
            listen.name, host_port,
            self.__render_config_block(listen.config_block))


    def render_frontend(self, frontend):
        frontend_str = '''
frontend %s %s

%s
        '''
        host_port = ''
        if not bool(frontend.config_block['binds']):
            host_port = '%s:%s' % (frontend.host, frontend.port)

        return frontend_str % (
            frontend.name, host_port,
            self.__render_config_block(frontend.config_block))

    def render_backend(self, backend):
        backend_str = '''

backend %s

%s
        '''
        return backend_str % (backend.name, self.__render_config_block(
            backend.config_block))

    def __render_config_block(self, config_block):
        """Summary

        Args:
            config_block ({'configs': list(tuple),
              'options': list(tuple),
              'servers': list(config.Server),
              'binds': list(config.Bind),
              'acls': list(config.Acl),
              'usebackends': list(config.UseBackend)
            }): Description

        Returns:
            str: config block str
        """
        config_block_str = ''
        for config_type, line_list in config_block.iteritems():
            for line in line_list:
                if config_type == 'options':
                    line_str = self.__render_option(line)
                elif config_type == 'configs':
                    line_str = self.__render_config(line)
                elif config_type == 'servers':
                    line_str = self.__render_server(line)
                elif config_type == 'binds':
                    line_str = self.__render_bind(line)
                elif config_type == 'acls':
                    line_str = self.__render_acl(line)
                elif config_type == 'usebackends':
                    line_str = self.__render_usebackend(line)
                # append line str
                config_block_str = config_block_str + line_str

        return config_block_str

    def __render_usebackend(self, usebackend):
        usebackend_line = '''
\t %s %s %s %s
'''
        backendtype = 'default_backend' if usebackend.is_default else 'use_backend'

        return usebackend_line % (
            backendtype, usebackend.backend_name,
            usebackend.operator, usebackend.backend_condition)

    def __render_server(self, server):
        server_line = '''
\t server %s %s:%s %s
'''
        return server_line % (
            server.name, server.host, server.port, ' '.join(server.attributes))

    def __render_acl(self, acl):
        acl_line = '''
\t acl %s %s
'''
        return acl_line % (acl.name, acl.value)

    def __render_bind(self, bind):
        bind_line = '''
\t bind %s:%s %s
'''
        return bind_line % (
            bind.host, bind.port, ' '.join(bind.attributes))

    def __render_option(self, option):
        option_line = '''
\t option %s %s
'''
        return option_line % (option[0], option[1])

    def __render_config(self, config):
        config_line = '''
\t %s %s
'''
        return config_line % (config[0], config[1])