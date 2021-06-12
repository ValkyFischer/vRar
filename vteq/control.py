# coding=utf-8

# ---------------------------------------------- #
# Title:            vRar                         #
# Description:      pack and unpack archives     #
# ---------------------------------------------- #
# Author:           fischer@valkyteq.com         #
# Date:             2021-03-28                   #
# Version:          1.0.0001                     #
# Copyright:        VALKYTEQ (c) 2021            #
# ---------------------------------------------- #


# imports
from vteq import utils
from os import walk, path, listdir, makedirs


def control():

	# Discover archives
	archives = discover([])
	dstPath = ""

	if archives is not []:

		# Write Log
		utils.logger(1, "Discovered archives:")
		for archive in archives:
			utils.logger(1, archive)

		# Load dir paths from config
		_, paths = utils.config("dst")
		for dstType, dstPath in paths[0].items():
			dstPath = dstPath

		# Path DOES exist
		try:
			next(walk(dstPath))

			for archive in archives:
				archiveName = path.splitext(path.basename(archive))[0]

				extractPath = dstPath + "\\" + archiveName

				try:
					if len(listdir(extractPath)):
						# Write Error Log
						utils.logger(9, "ERROR: {err}".format(err="UnrarError"))
						utils.logger(9, "Destination Path {path} is not empty.".format(path=extractPath))
				except WindowsError:
					# Write Log
					utils.logger(1, "Unpacking archives '{archive}' to {path}".format(archive=archive, path=extractPath))

					if not path.exists(extractPath):
						makedirs(extractPath)

					utils.unrar(archive, extractPath)

		# Path DOES NOT exist
		except StopIteration:
			# Write Error Log
			utils.logger(9, "ERROR: {err}".format(err="ConfigError"))
			utils.logger(9, "Destination Path {path} does not exist.".format(path=dstPath))


# Find all files
def discover(archives, dirs=None):
	"""
	- Discovers all files based on paths in config
	- Finds files in all subfolder
	:param list archives: List of files
	:param str dirs: Optional: Directory names
	:return: List of rar archives
	"""

	# IMPORTANT: Enter this, when dir path IS known
	if dirs is not None:
		srcPath = dirs

		# Path DOES exist
		try:
			_, dirnames, filenames = next(walk(srcPath))

			# Discover files
			for files in filenames:
				_, ext = path.splitext(files)
				# Append to return list if file extension matches
				if ext == ".rar":
					archives.append(srcPath + "\\" + files)

			# Discover dirs
			for dirs in dirnames:
				# Run itself with discovered sub dir
				discover(archives, srcPath + "\\" + dirs)

		# Path DOES NOT exist
		except StopIteration:
			# Write Error Log
			utils.logger(9, "ERROR: {err}".format(err="ConfigError"))
			utils.logger(9, "Path {path} does not exist.".format(path=srcPath))

	# IMPORTANT: Enter this, when dir path IS NOT known
	else:
		# Load dir paths from config
		_, paths = utils.config("src")
		for srcType, srcPath in paths[0].items():
			if srcPath is not "":
				# Write Log
				utils.logger(1, "Found path for '{type}' in config: {path}".format(path=srcPath, type=srcType))
				# Run itself with dir path from config
				discover(archives, srcPath)

	# Return list of archives, after all files in all subfolders are discovered
	return archives
