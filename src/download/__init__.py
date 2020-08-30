import sys
sys.path.append('/home/zy/Rpi3BAndSamb')

import src.download.you_get_shell
import src.download.aria2_shell


def you_get_download(args):
    src.download.you_get_shell.main(args)

def aria2_download(args):
    src.download.aria2_shell.main(args)