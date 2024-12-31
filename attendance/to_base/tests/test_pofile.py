import glob

from odoo.modules import get_modules, get_resource_path
from odoo.tests.common import TransactionCase
from odoo.tools.translate import TranslationFileReader


class TestPOFiles(TransactionCase):

    def iter_module_pofiles(self):
        """ Yields the paths of all the module pofiles
        """
        for module in get_modules():
            fnames = []

            if get_resource_path(module, 'i18n'):
                fnames.extend(glob.glob(get_resource_path(module, 'i18n') + '/*.po'))

            if get_resource_path(module, 'i18n_extra'):
                fnames.extend(glob.glob(get_resource_path(module, 'i18n_extra') + '/*.po'))

            yield from fnames

    def test_pofiles_string_formatting(self):
        # retrieve all modules, and their corresponding PO files
        pofiles_to_check = sorted([p for p in self.iter_module_pofiles()])

        error = ''
        for filename in pofiles_to_check:
            msg = ''
            for poline in TranslationFileReader(filename).pofile:
                if poline.msgstr and poline.msgid and poline.msgid.count('%s') != poline.msgstr.count('%s'):
                    msg += f'\nmsgid:\n{poline.msgid}\nmsgstr:\n{poline.msgstr}\n'
            if msg:
                msg = f'\n{filename}:\n' + msg
                error += msg
        if error:
            self.fail("Number of '%s' between msgid and msgstr is not equal:\n" + error)
