import sys
import googletrans as gt
from PyQt5.QtWidgets import QApplication, QMainWindow
from gui import UiMainWindow

app = QApplication(sys.argv)
window = QMainWindow()
ui = UiMainWindow()
ui.setupUi(window)

window.show()

ui.cmbTranslateFrom.clear()
ui.cmbTranslateFrom.addItems([i.capitalize() for i in gt.LANGCODES])
ui.cmbTranslateFrom.setCurrentText('English')
ui.cmbTranslateTo.clear()
ui.cmbTranslateTo.addItems([i.capitalize() for i in gt.LANGCODES])
ui.cmbTranslateTo.setCurrentText('Polish')

tr = gt.Translator()


def swap_languages():
    lang_from = ui.cmbTranslateFrom.currentText()
    lang_to = ui.cmbTranslateTo.currentText()
    ui.cmbTranslateFrom.setCurrentText(lang_to)
    ui.cmbTranslateTo.setCurrentText(lang_from)


def go():
    word = ui.txtOrigin.toPlainText()
    if word != '':
        src = gt.LANGCODES[ui.cmbTranslateFrom.currentText().lower()]
        dest = gt.LANGCODES[ui.cmbTranslateTo.currentText().lower()]
        trans = tr.translate(word, dest, src)
        translation = trans.extra_data['translation'][0][0]
        ui.txtTranslations.setText(translation)
        try:
            translations = trans.extra_data['all-translations'][0][2]
            for v, translation in enumerate(translations):
                if v == 0:
                    ui.txtOther.setText(translation[0] + ' ---> ' + ', '.join(translation[1:][0]))
                else:
                    ui.txtOther.append(translation[0] + ' ---> ' + ', '.join(translation[1:][0]))
        except:
            ui.txtOther.clear()

        definitions = trans.extra_data['definitions']
        if definitions is not None:
            for item in definitions:
                part_of_speech = item[0]
                ui.txtDefinitions.setText(part_of_speech + '\n')
                for v, i in enumerate(item[1]):
                    definition = i[0]
                    try:
                        example = i[2]
                    except IndexError:
                        example = ''
                    finally:
                        ui.txtDefinitions.append(str(v + 1) + '. ' + definition)
                        ui.txtDefinitions.append('example: ' + example)
        else:
            ui.txtDefinitions.clear()

        synonyms = trans.extra_data['synonyms']
        if synonyms is not None:
            for v, i in enumerate(synonyms):
                try:
                    if v == 0:
                        ui.txtSynonyms.setText(i[0] + ' ----> ' + ', '.join(i[1][0][0]))
                    else:
                        ui.txtSynonyms.append(i[0] + ' ----> ' + ', '.join(i[1][0][0]))
                except:
                    pass
        else:
            ui.txtSynonyms.clear()

        examples = trans.extra_data['examples']
        if examples is not None:
            for v, i in enumerate(examples[0]):
                ex = i[0].replace('<b>' + word + '</b>', word)
                if v == 0:
                    ui.txtExamples.setText(ex)
                else:
                    ui.txtExamples.append(ex)
        else:
            ui.txtExamples.clear()

    else:
        ui.txtTranslations.clear()
        ui.txtOther.clear()
        ui.txtDefinitions.clear()
        ui.txtSynonyms.clear()
        ui.txtExamples.clear()


ui.btnSwap.clicked.connect(swap_languages)
ui.txtOrigin.textChanged.connect(go)
ui.cmbTranslateFrom.currentIndexChanged.connect(go)
ui.cmbTranslateTo.currentIndexChanged.connect(go)
sys.exit(app.exec_())
