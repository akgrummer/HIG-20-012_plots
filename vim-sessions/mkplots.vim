let SessionLoad = 1
let s:so_save = &g:so | let s:siso_save = &g:siso | setg so=0 siso=0 | setl so=-1 siso=-1
let v:this_session=expand("<sfile>:p")
silent only
silent tabonly
cd /uscms_data/d3/agrummer/DiHiggs_v2/CMSSW_10_2_5/src/bbbbAnalysis/HIG-20-012_plots
if expand('%') == '' && !&modified && line('$') <= 1 && getline(1) == ''
  let s:wipebuf = bufnr('%')
endif
let s:shortmess_save = &shortmess
if &shortmess =~ 'A'
  set shortmess=aoOA
else
  set shortmess=aoO
endif
badd +7 .gitignore
badd +38 README.md
badd +17 sync.sh
badd +4 run/multiPadPlots.sh
badd +62 src/plotDistributions.py
badd +1 src/VariableDicts.py
badd +216 src/PlotLimitVsMy_orig_multiPad.py
badd +4 run/HHplot.sh
badd +61 src/PlotLimitVsMy_orig.py
badd +3 run/theoryComparison.sh
badd +256 src/Plot2DLimitMap.C
badd +493 src/plot1Dvars.py
badd +1 /uscms_data/d3/agrummer/DiHiggs_v2/CMSSW_10_2_5/src/bbbbAnalysis/HIG-20-012_plots/./run/createNMSSMrootfile.sh
badd +31 src/NMSSMrootfile.C
badd +1 input/NMSSMdata.csv
argglobal
%argdel
$argadd .gitignore
edit README.md
argglobal
balt src/NMSSMrootfile.C
setlocal fdm=expr
setlocal fde=MarkdownLevel(v:lnum)
setlocal fmr={{{,}}}
setlocal fdi=#
setlocal fdl=0
setlocal fml=1
setlocal fdn=20
setlocal nofen
let s:l = 49 - ((41 * winheight(0) + 22) / 45)
if s:l < 1 | let s:l = 1 | endif
keepjumps exe s:l
normal! zt
keepjumps 49
normal! 0
tabnext 1
if exists('s:wipebuf') && len(win_findbuf(s:wipebuf)) == 0 && getbufvar(s:wipebuf, '&buftype') isnot# 'terminal'
  silent exe 'bwipe ' . s:wipebuf
endif
unlet! s:wipebuf
set winheight=1 winwidth=20
let &shortmess = s:shortmess_save
let s:sx = expand("<sfile>:p:r")."x.vim"
if filereadable(s:sx)
  exe "source " . fnameescape(s:sx)
endif
let &g:so = s:so_save | let &g:siso = s:siso_save
set hlsearch
doautoall SessionLoadPost
unlet SessionLoad
" vim: set ft=vim :
