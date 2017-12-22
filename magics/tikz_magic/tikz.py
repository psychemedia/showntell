#via https://github.com/robjstan/tikzmagic
import subprocess
import shlex
import shutil
import tempfile
from argparse import ArgumentParser
from base64 import b64encode
from os.path import isfile
from os import getcwd

from IPython.core.magic import (
    magics_class, line_magic, line_cell_magic, Magics)
from IPython.core.display import Image, HTML

LATEX_TEMPLATE = r'''
\documentclass[tikz,border={border}]{{standalone}}
\usepackage{{tikz,{latex_pkgs}}}
\usetikzlibrary{{{tikz_libs}}}
{latex_pre}
\begin{{document}}
{content}
\end{{document}}'''

        
@magics_class
class TikzMagic(Magics):
    def __init__(self, shell, cache_display_data=False):
        super(TikzMagic, self).__init__(shell)
        self.cache_display_data = cache_display_data


    @line_cell_magic
    def tikz(self,line, cell=''):
        '''Format TikZ commands into a LaTeX document, compile, and convert.'''
        parser = ArgumentParser()
        parser.add_argument('-p', '--latex_packages', default='')
        parser.add_argument('-x', '--latex_preamble', default='')
        parser.add_argument('-l', '--tikz_libraries', default='')
        parser.add_argument('-i', '--input_file', default=None)
        parser.add_argument('-e', '--export_file', default=None)
        parser.add_argument('-s', '--scale', default=1, type=float)
        parser.add_argument('-b', '--border', default=4)
        parser.add_argument('-v', '--variable', default=None)
        parser.add_argument('--wrap', dest='wrap_env', action='store_true')
        parser.add_argument('--no-wrap', dest='wrap_env', action='store_false')
        parser.set_defaults(wrap_env=True)
        parser.add_argument('--debug', dest='debug_mode', action='store_true')
        parser.set_defaults(debug_mode=False)
        args = parser.parse_args(shlex.split(line))

        # prepare latex from template
        if args.input_file:
            # add content from input_file before rest of cell
            cell += r'\input{{{cwd}/{file}}}'.format(cwd=getcwd(),
                                                     file=args.input_file)

        if args.variable:
            cell = self.shell.user_ns[args.variable]
            
        if args.wrap_env:
            cell = r'\begin{tikzpicture}' + cell + r'\end{tikzpicture}'

        latex = LATEX_TEMPLATE.format(content=cell,
                                      border=args.border,
                                      latex_pre=args.latex_preamble,
                                      latex_pkgs=args.latex_packages,
                                      tikz_libs=args.tikz_libraries)

        if args.debug_mode:
            print(latex)

        # add current working directory to any export_file path
        if args.export_file:
            args.export_file = getcwd() + '/' + args.export_file

        # compile and convert, returning Image data
        return latex2image(latex, int(args.scale*300), args.export_file)

def latex2image(latex, density, export_file=None):
    '''Compile LaTeX to PDF, and convert to PNG.'''
    try:
        # make a temp directory, and name temp files
        temp_dir = tempfile.mkdtemp()
        temp_tex = temp_dir + '/tikzfile.tex'
        temp_pdf = temp_dir + '/tikzfile.pdf'
        temp_png = temp_dir + '/tikzfile.png'

        open(temp_tex, 'w').write(latex)
        # run LaTeX to generate a PDF
        sh_latex(in_file=temp_tex, out_dir=temp_dir)

        if not isfile(temp_pdf):
            raise Exception('pdflatex did not produce a PDF file.')

        if export_file:
            shutil.copyfile(temp_pdf, export_file)

         # convert PDF to PNG
        sh_convert(in_file=temp_pdf, out_file=temp_png, density=density)
        
        #The Image(data=png) thing doesn't work..?
        png = b64encode(open(temp_png, "rb").read())
        #return Image(data=png)
        return Image(filename=temp_png)
        
    finally:
        # remove temp directory
        shutil.rmtree(temp_dir)

# functions to run command line scripts
def sh_latex(in_file, out_dir):
    '''Compile XeLaTeX to generate a PDF.'''
    subprocess.call(['xelatex', '-output-directory', out_dir, in_file])

def sh_convert(in_file, out_file, density=96):
    '''Use ImageMagick to convert PDF to PNG.'''
    subprocess.call(['convert', '-density', str(density), in_file, out_file])

def load_ipython_extension(ipython):
    ipython.register_magics(TikzMagic)
    
ip = get_ipython()
ip.register_magics(TikzMagic)