#!/bin/sh

# Converting PDF to PostScript file
pdftops $1 > lpr -Ppstsb
