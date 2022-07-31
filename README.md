# Python3 Helpers

Some Classes for Python3


## Usage

	git submodule add https://github.com/hilbix/py3.git


## Notes

- `DoubleLinked.List` is what the name suggests
  - This is mostly `O(1)` for all operations except indexed access
  - There is no indexed access (yet)

`Data.Object` implements convenient Objects, like:

- `o = Data.Object(a=1)`
  - `o.a == 1`
  - `o['a'] == 1`
- `o = Data.Object(*"xyz")`
  - `o[0] == 'x'`
  - `o[1] == 'y'`
  - `o[2] == 'z'`


## FAQ

WTF why?

- Because I need it

License?

- This Works is placed under the terms of the Copyright Less License,  
  see file COPYRIGHT.CLL.  USE AT OWN RISK, ABSOLUTELY NO WARRANTY.
- Read: Free as free beer, free speech, free baby

