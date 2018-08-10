" ============================================================================
" File:        vimusic.vim
" Description: plugin for music compose
" Author:      Lei Liu <liunx163@163.com>
" Licence:     Vim licence
" Website:     http://github.com/liunx/vimusic/
" Version:     0.1.0
" ============================================================================

scriptencoding utf-8

if exists("loaded_vimusic")
    finish
endif
let loaded_vimusic = 1

if v:version < 700
    echohl WarningMsg
    echomsg 'Vimusic: Vim version is too old, Vimusic requires at least 7.0'
    echohl None
    finish
endif

if !has('python3')
    echohl WarningMsg
    echomsg 'Vimusic: Need python3 support!'
    echohl None
    finish
endif

function! s:say_hello() abort
    echo 'Do~, Re~, Mi~, Fa~, Sol, La, Si, Do'
endfunction


" Commands 
command! -nargs=0 SayHello             call s:say_hello()

" vim: ts=8 sw=4 sts=4 et foldenable foldmethod=marker foldcolumn=1
