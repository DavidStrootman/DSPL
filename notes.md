### Rust lexer
#### Basic lexing
In the rust lexer all tokens are created from a stream of chars, which is made peekable. All tokens are made by calling
[Advance token](https://doc.rust-lang.org/stable/nightly-rustc/rustc_lexer/cursor/struct.Cursor.html#method.advance_token).
This function has most of the logic on how most tokens are created. This is probably the most "magic" function in the
lexer since it holds all the rules on lexing.



The rust lexer seems the handle keywords by first parsing them as literals and then "unescaping" them.  
https://doc.rust-lang.org/stable/nightly-rustc/rustc_lexer/unescape/index.html


This function cooks the basic lexer tokens into rich or wide lexer tokens  
https://doc.rust-lang.org/stable/nightly-rustc/src/rustc_parse/lexer/mod.rs.html#157  
This expansion seems to be purely for keeping the code simple and easy to read.  
The file is lexed twice, only adding more information to tokens the second way round.