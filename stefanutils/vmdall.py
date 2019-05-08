from moleculekit.molecule import Molecule
from natsort import natsorted
from glob import glob
import os
import sys
import argparse

# the order in the list defines priorities
trajformats = ['dcd', 'xtc',]
topoformats = ['psf', 'prmtop', 'pdb']
coorformats = ['coor', 'pdb']

def getArgumentParser():
    parser = argparse.ArgumentParser(description='Stefan\'s VMD viewer')
    parser.add_argument('-d', type=int, dest='maxdepth', default=2, help='Max depth of trajectory search')
    parser.add_argument('-nf', action='store_true', help='If used it will disable water filtering')
    parser.add_argument('-li', type=str, default='', help='Atomselection for licorice representations')
    return parser
    

def findFiles(formats, maxdepth):
    allfiles = []
    for i in range(1, maxdepth+1):
        for ff in formats:
            allfiles += list(glob('*{}.{}'.format('/*' * i, ff)))
    return allfiles

def createFolderDictionary(alltraj, alltopo, allcoor):
    from collections import defaultdict
    folderdict = defaultdict(lambda: defaultdict(list))
    for file in alltraj:
        dirname = os.path.dirname(file)
        ext = os.path.splitext(file)[-1][1:]
        folderdict[dirname]['traj'+ext].append(file)

    for file in alltopo:
        dirname = os.path.dirname(file)
        ext = os.path.splitext(file)[-1][1:]
        if ext in folderdict[dirname]:
            raise RuntimeError('Two {} topologies found in folder: {}'.format(ext, dirname))
        folderdict[dirname]['topo'+ext] = file

    for file in allcoor:
        dirname = os.path.dirname(file)
        ext = os.path.splitext(file)[-1][1:]
        if ext in folderdict[dirname]:
            raise RuntimeError('Two {} coordinate files found in folder: {}'.format(ext, dirname))
        folderdict[dirname]['coor'+ext].append(file)
    return folderdict

def main(arguments=None):
    parser = getArgumentParser()
    args = parser.parse_args(args=arguments)

    alltraj = findFiles(trajformats, args.maxdepth)
    alltopo = findFiles(topoformats, args.maxdepth)
    allcoor = findFiles(coorformats, args.maxdepth)
    folderdict = createFolderDictionary(alltraj, alltopo, allcoor)

    for folder in natsorted(folderdict):
        mol = None
        for topo in topoformats:
            if 'topo'+topo in folderdict[folder]:
                mol = Molecule(folderdict[folder]['topo'+topo])
                break
        if mol is None:
            print('No topology found in {}'.format(folder))
            continue
        foundtraj = False
        for traj in trajformats:
            if 'traj'+traj in folderdict[folder]:
                mol.read(natsorted(folderdict[folder]['traj'+traj]))
                foundtraj = True
                break
        if not foundtraj:
            for coor in coorformats:
                if 'coor'+coor in folderdict[folder]:
                    mol.read(folderdict[folder]['coor'+coor])
                    break
        if mol.numFrames == 0:
            print('No coordinates found in {}'.format(folder))
            continue

        if not args.nf:
            mol.filter('not water')
        mol.viewname = folder
        mol.view(style='NewCartoon', sel='protein', hold=True)
        mol.view(style='Lines', sel='not protein and not water', hold=True)
        if args.li != '':
            mol.view(style='Licorice', sel=args.li, hold=True)
        mol.view()

    input('Press any button to exit.')



if __name__ == '__main__':
    import sys
    main(arguments=sys.argv[1:])