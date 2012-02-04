import logging
from inspect import getmembers
from os.path import join, exists, dirname
from os import makedirs

from django.core.management.base import BaseCommand
from django.utils.importlib import import_module
from devilry.apps import extjshelpers

from devilry.restful import RestfulManager
from devilry.utils.command import setup_logging, get_verbosity
from devilry.utils.importutils import get_installed_apps
from devilry.apps.extjshelpers.modelintegration import (restfulcls_to_extjsmodel,
                                                        get_extjs_modelname)


def get_restful_apps():
    apps = []
    for moddir, mod, appname in get_installed_apps():
        try:
            restfulmodule = import_module('{0}.{1}'.format(mod.__name__, 'restful'))
        except ImportError, e:
            pass
        else:
            apps.append((moddir, restfulmodule, appname))
    return apps


class Command(BaseCommand):
    help = 'Autogenerate ExtJS models from restful interfaces.'

    fileheader = '// Autogenerated by the dev_coreextjsmodels script. DO NOT CHANGE MANUALLY'

    def handle(self, *args, **options):
        setup_logging(get_verbosity(options))
        all_modelnames = self._create_files_for_all_modules(get_restful_apps())
        self._create_requireall_file(all_modelnames)

    def _create_files_for_all_modules(self, restful_apps):
        all_modelnames = []
        for moddir, restfulmodule, appname in restful_apps:
            modelnames = self._create_files_for_module(moddir, restfulmodule, appname)
            all_modelnames += modelnames
        return all_modelnames

    def _create_files_for_module(self, moddir, restfulmodule, appname):
        modelnames = []
        logging.info('Parsing app: %s', appname)
        self._get_restfulmanagers(restfulmodule)
        for restfulmanager in self._get_restfulmanagers(restfulmodule):
            for restfulcls in restfulmanager.iter_restfulclasses():
                logging.debug('Generating JS code for: %s', restfulcls.__name__)
                js = self._get_js_for_model(restfulcls)
                modelname = get_extjs_modelname(restfulcls)
                self._create_extjsclassfile(moddir, modelname, js)
                modelnames.append(modelname)
        return modelnames

    def _get_restfulmanagers(self, restfulmodule):
        def is_restfulmananager_obj(obj):
            return isinstance(obj, RestfulManager)
        return [manager for name, manager in getmembers(restfulmodule, is_restfulmananager_obj)]

    def _create_requireall_file(self, modelnames):
        extjshelpersdir = dirname(extjshelpers.__file__)
        requires = ',\n'.join(["    '{0}'".format(modelname) for modelname in modelnames])
        content = ('{{% comment %}}\n'
                   '{0}\n'
                   '// This is a Django template because we want to make it easy to dump it into the page template.\n'
                   '{{% endcomment %}}'
                   '\nExt.require([\n{1}\n]);').format(self.fileheader, requires)
        dirpath = join(extjshelpersdir, 'templates', 'extjshelpers')
        path = join(dirpath, 'restful-generated-models.django.js')
        logging.info('Creating: %s', path)
        logging.debug('%s: %s', path, content)
        makedirs(dirpath)
        open(path, 'w').write(content)

    def _get_js_for_model(self, restfulcls):
        result_fieldgroups =  restfulcls._meta.simplified._meta.resultfields.additional_aslist()
        js = restfulcls_to_extjsmodel(restfulcls, result_fieldgroups, pretty=True)
        return js + ';'

    def _create_extjsclass_dir(self, moddir, modelname):
        path = modelname.split('.')[1:-1]
        directory = join(moddir, 'static', 'extjs_classes', *path)
        if not exists(directory):
            logging.info('Creating directory: %s', directory)
            makedirs(directory)
        return directory

    def _create_extjsclassfile(self, moddir, modelname, js):
        directory = self._create_extjsclass_dir(moddir, modelname)
        clsname = modelname.split('.')[-1]
        data = '{0}\n{1}'.format(self.fileheader, js)
        path = join(directory, clsname + '.js')
        logging.info('Creating: %s', path)
        logging.debug('%s: %s', path, data)
        open(path, 'w').write(data)
