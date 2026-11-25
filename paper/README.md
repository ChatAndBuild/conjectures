# Paper

`conjectures.tex` describes how the work was organised: agent roles, the problem atlas, the RSI
Ralph loop, memory, and how each target was broken down. `conjectures.pdf` is the compiled
version. The mathematics is in the repositories; the detailed proof for Erdős 985 is in
[erdos-985/paper](https://github.com/senamakel/erdos-985/tree/main/paper).

To rebuild the PDF, use [tectonic](https://tectonic-typesetting.github.io):

```bash
cd paper
tectonic conjectures.tex
```

Any standard TeX distribution also works (`pdflatex conjectures.tex`, run twice for references).
