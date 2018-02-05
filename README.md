# python_propertyutils

## How to use:

Creates a property called `myprop`, internally stored as `_myprop`,
that is instantiated only once, read only, and return the value
`DefaultValue()`

```
@lazyproperty('_myprop')
def myprop(self):
    return DefaultValue()

self.myprop == <instance DefaultValue>
```

Optionally, the store name can be omitted, in this case the name used
to store the value will be the name given for this property with a `_`
(underscore) in front of it. The code bellow creates exactly the same
property (with the same persistence name used) as the code above:

```
@lazyproperty()
def myprop(self):
    return DefaultValue()

self.myprop == <instance DefaultValue>
```

Creates a property called `myprop2`, internally stored as `_myprop2`,
that accepts being set, but, if no value is given to it, it returns
'DefaultValue()', and can be deleted, with causes it to return its default
value

```
@lazyproperty('_myprop2', fset=True, fdel=True)
def myprop2(self):
    return DefaultValue()

self.myprop2 == DefaultValue()
self.myprop2 = 10
self.myprop2 == 10
del self.myprop2
self.myprop2 == DefaultValue()
```

Creates a property called myprop3, internally stored as `_FOO`,
that accepts being set but only if is `basestring`, then append a string
at the end. It also cannot be deleted.

```
def myprop3(self, value):
    if not isinstance(value, basestring):
        raise Exception('NOOOO')
    return value + ' software engineer'

@lazyproperty('_FOO', fset=True, fdel=True)
def myprop3(self):
    return 'No one'

self.myprop3 == 'No one'
self.myprop3 = 'Jean Schmidt'
self.myprop3 == 'Jean Schmidt software engineer'
self.myprop3 = 10
Traceback(....)
del self.myprop3
Traceback(....)
self.myprop3 == 'Jean Schmidt software engineer'
```
