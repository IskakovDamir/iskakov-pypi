# iskakov

`pip install iskakov` installs [`own-baseline`](https://pypi.org/project/own-baseline/)
and gives you its command line under a second name. The two names run the same
program:

```bash
pip install iskakov

iskakov    check cells.h5ad --score obs:ccat --ordinal obs:stage \
                            --primitive degree-corr --ordinal-source experimental
ownbaseline check ...        # identical
```

Import the real package in scripts:

```python
from own_baseline import conditional_skill_report
```

## What the tool does

A potency score is supposed to order single cells by developmental potential.
Most published scores are built on a low-order primitive of the same expression
matrix: the number of genes detected, the correlation of a cell's profile with
network node degree, the Shannon entropy of the profile, the library size.
`own-baseline` asks whether the score orders a held-out ordinal any better than
that primitive does on its own. It rank-residualizes the score on its
author-declared primitive, takes Kendall's tau_b against the ordinal, and
compares the result against a measured floor from a 200-seed null grid indexed
by sample size, rank correlation, kernel and covariate count. The floor table
ships inside the wheel, so the answer does not depend on a network call.

Four verbs: `check`, `floors`, `primitives`, `verify`.

## Where the code lives

Source, tests, the null grid and the documentation are in the `own-baseline`
repository. This distribution is 60 lines of forwarding.

MIT licensed.
