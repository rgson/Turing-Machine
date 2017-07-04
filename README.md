# Turing Machine Prototype

A virtual Turing Machine with it's own basic programming language.

## Language

Programs are specified in a simple programming language.

### Example

    // Example program

    foo [start]
        1 -> 0 L foo
        0 -> 1 L foo
        _ -> _ S bar

    bar [halt]

The example program inverts a binary number; all `1`s are replaced by `0`s and vice versa.

1. The program starts in the `foo` state, which is signalled by the `[start]` tag.
    * If a `1` is read, the machine will write `0`, move the tape one step to the `L`eft and transition to the `foo` state (i.e. repeat the same state).
    * If a `0` is read, the machine will write a `1` instead, move the tape to the left and repeat the `foo` state.
    * If a blank space (`_`) is encountered, the blank character is written, the tape is not moved (`S`tay) and the machine transitions to the `bar` state.
2. The machine halts upon entering the `bar` state, as signalled by the `[halt]` tag.

### Description

* **States** are defined by a textual (alphanumeric) identifier. *Example:* `foo`
* **Instructions** occur within states and are triggered by a read character. They consist of one write, one move and one state transition. *Example:* `1 -> 0 L foo`
* **Symbols** constitute the alphabet used for reads and writes. They may be chosen arbitrarily. Underscore (`_`) is used as the default, "blank" symbol. *Example:* `1`
* **Moves** express the movement of the virtual magnetic tape, moving it either `L`eft or  `R`ight. Alternatively, the tape can `S`tay at the current location.
* **Transitions** change the machine's state to alter its behavior.
* **Tags** express certain meta-data about states, i.e. where the program starts (`[start]`) and where it ends (`[halt]`).
    If `[start]` is omitted, the first state is assumed to be the start state. If `[halt]` is omitted, a `halt` state will be implicitly defined to fill the role.
* **Comments** start with `//` and last until the next line break.
