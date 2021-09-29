" diffget is pretty silly, there's no good way to just copy the diff block
" into your region.  so, use a hack via undo + copy + paste:
"
" \2 puts the diff in window 2 after the diff in the current window
" ctrl-\2 replaces the diff in the window with the diff in window 2, and also
" puts the old contents of the current window into the paste buffer.
" That way you can paste it anywhere in the file.
"
map \3 :diffget 3<CR>u:'[,']y<CR>:diffupdate<CR>:diffget 3<CR>P:diffupdate<CR>
map <C-\>3 :diffget 3<CR>u:'[,']y<CR>:diffupdate<CR>:diffget 3<CR>:diffupdate<CR>

map \2 :diffget 2<CR>u:'[,']y<CR>:diffupdate<CR>:diffget 2<CR>P :diffupdate<CR>
map <C-\>2 :diffget 2<CR>u:'[,']y<CR>:diffupdate<CR>:diffget 2<CR>:diffupdate<CR>

map \1 :diffget 1<CR>u:'[,']y<CR>:diffupdate<CR>:diffget 2<CR>P:diffupdate<CR>
map <C-\>1 :diffget 1<CR>u:'[,']y<CR>:diffupdate<CR>:diffget 1<CR>:diffupdate<CR>

