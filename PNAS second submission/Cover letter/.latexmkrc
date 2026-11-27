# Write SyncTeX data on every build, however it is started.
#
# LaTeX Workshop passes -synctex=1 itself, but a plain `latexmk -pdf` from a
# terminal does not. A build without it deletes the existing .synctex.gz, and
# the editor's next build then sees an up-to-date PDF and does not write a new
# one, so jumping between the PDF and the source stops working until the
# source changes again. Setting the flag here makes every build the same.
$pdf_mode = 1;
$pdflatex = 'pdflatex -synctex=1 %O %S';
