import os

import re
import matplotlib
import matplotlib.pyplot as plt
plt.get_backend()

def formula2img(str_latex, out_file, img_size=(5,3), font_size=5):
    fig = plt.figure(figsize=img_size)
    ax = fig.add_axes([0, 0, 1, 1])
    ax.get_xaxis().set_visible(False)
    ax.get_yaxis().set_visible(False)
    ax.set_xticks([])
    ax.set_yticks([])
    plt.text(0.5, 0.5, str_latex, fontsize=font_size, verticalalignment='center', horizontalalignment='center')
    plt.savefig(out_file)

def get_max_str(lst):
    return max(lst, key=len)


def formula2png(str_latex):
    # str_latex = '有一个公式是 \'$ \sum_{a}^{b} $ \',另一个公式是$\sum_{b}^{c}$'
    # str_latex = re.findall(r'\$([^\$]*)\$', str_latex)
    # str_latex = get_max_str(str_latex)
    str_latex = str_latex.replace(".\n",";")
    str_latex = '$'+str_latex+'$'
    str_latex = str_latex.replace("\\text", "")
    str_latex = str_latex.replace("\\land", "\\wedge")
    str_latex = str_latex.replace("\\implies", "\\rightarrow")
    str_latex = str_latex.replace("\\lnot", "\\neg")
    # str_latex = r'$\neg({zhedang} \wedge {auto\_control\_mode}) \Rightarrow  {G}(\neg  {auto\_control})$'
    BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
    path_dir = BASE_DIR + '\\static\\blog\\images\\home\\fl.png'
    formula2img(str_latex, path_dir, img_size=(18,3), font_size=15)
