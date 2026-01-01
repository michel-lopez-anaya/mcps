version 6.0
if &cp | set nocp | endif
map  :w
let s:cpo_save=&cpo
set cpo&vim
xnoremap gx <ScriptCmd>vim9.Open(getregion(getpos('v'), getpos('.'), { type: mode() })->join())
nnoremap gx <ScriptCmd>vim9.Open(GetWordUnderCursor())
map <C-S> :w
let &cpo=s:cpo_save
unlet s:cpo_save
set expandtab
set fileencodings=ucs-bom,utf-8,default,latin1
set helplang=fr
set nomodeline
set ruler
set runtimepath=~/.vim,/var/lib/vim/addons,/etc/vim,/usr/share/vim/vimfiles,/usr/share/vim/vim91,/usr/share/vim/vim91/pack/dist/opt/netrw,/usr/share/vim/vimfiles/after,/etc/vim/after,/var/lib/vim/addons/after,~/.vim/after
set shiftwidth=4
set suffixes=.bak,~,.swp,.o,.info,.aux,.log,.dvi,.bbl,.blg,.brf,.cb,.ind,.idx,.ilg,.inx,.out,.toc
set tabstop=4
" vim: set ft=vim :
