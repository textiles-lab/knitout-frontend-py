# knitout-frontend-py
 

A python wrapper for all operations supported by knitout with basic error and type checking.
To use import the `knitout`	module. See  `knitout.example()` for example usage.


```python example
import knitout 
w = knitout.Writer('1 2 3')
w.ingripper('1')
w.knit('+',('f',0),1)
...
w.write('out.k')
```


In the table below:

* `carriers`  specify the yarn-carriers in use. These are specified as a string or an Array of strings. Multiple yarn carriers can be used to make one stitch ("plating").

* `direction`  specifies the direction in which the operation is performed. Legal values include **"+"** indicating increasing needle number direction or **"-"** indicating decreasing needle number direction.

* `bed+needle` is an alpha-numeric value that specifies the bed and needle number.
Legal values for `bed` are (**f**)ront, (**b**)ack,  (**f**)ront(**s**)lider, (**b**)ack(**s**)lider.
Needle is a Number value within the range supported by the machine.
"fs10", for example, specifies front-bed slider location 10, "b20" specifies back-bed needle 20.
The front-end also allows specifying bed needles as tuples  `("f",5)` or lists `["f",5]`.
A valid set of carriers need to be initialized when creating a Writer object.

All knitout opcodes are supported as a front-end function. Currently, the frontend supports:

Function | Arguments | Example | Description
--- | --- | --- | ---
addHeader | `name`(String),`value`(String) |  addHeader('Machine', 'SWGXYZ')| Add header information as name,value pairs. This is also used for including [extensions](https://textiles-lab.github.io/knitout/extensions.html).
ingripper  | `carriers` | ingripper("5") | Bring in yarn carriers
inhook | `carriers` | inhook("B") | Bring in yarn carriers using the yarn inserting hook
releasehook    | `carriers` | releasehook("5") | Release the yarn inserting hook used to bring in the given yarn carriers
outgripper | `carriers` | outgripper("6") | Take out yarn carrier
outhook | `carriers` | outhook("5") | Take out yarn carrier with yarn inserting hook
stitchNumber|`index`(Number)  | stitchNumber(5) | Explicit function for using stitch number extension that reads stitch values at `index` from a table. See [extensions](https://textiles-lab.github.io/knitout/extensions.html) for details.
fabricPresser|`mode`(String)  | fabricPresser('auto') | Explicit function for using fabric presser extension. Valid modes include 'auto', 'on', 'off'. See [extensions](https://textiles-lab.github.io/knitout/extensions.html) for details.
rack | `rack value`(Number) | rack(1) | Translate the back bed relative to the front bed by `rack value` needle units. Fractional values are legal and may be supported by the machine.
tuck | `direction`,`bed+needle`,`carriers` | tuck("+","f10","B") | Tuck on `bed` at `needle` using `carriers` in `direction` direction. 
knit | `direction`,`bed+needle`,`carriers` | knit("+","f10","B") | Knit on `bed` at `needle` using `carriers` in `direction` direction. 
xfer | `from bed+needle`,`to bed+needle` | xfer("f10","b10") | Transfer loops from `from bed` at `needle` to  `to bed` at `needle`. 
miss | `direction`,`bed+needle`,`carriers` | miss("+","f10","B") | Miss on `bed` at `needle` using `carriers` in `direction` direction i.e., perform carrier motion without knitting
split| `direction`,`from bed+needle`,`to bed+needle`, `carriers` | split("+","f10", "b10", "B") | Pull a loop from `from bed+needle` and transfer old loops to `to bed+needle` in   `direction` using `carriers`. 
drop| `bed+needle`| drop("f10") | Drop loops from `bed+needle`.
amiss| `bed+needle`| amiss("f10") | Tuck operation at `bed+needle` without using yarn. 
pause| None | pause() | Pause machine when instruction is encountered
comment| String | comment("This is a comment") | Insert comments into knitout file
addRawOperation| String | addRawOperation("your knitout inst string") | Escape hatch to directly inject knitout code  


See [knitout specification](https://textiles-lab.github.io/knitout/knitout.html) for further details.

See knitout.example() for example usage of this frontend to create stockinette, garter and rib rectangles.
