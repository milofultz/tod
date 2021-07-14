# Tod

Plan and manage daily tasks. Deliberately simple so I can stay focused on what I need to do. 

* Saves tasks in an easy to read plaintext file in the root folder called `~/.tod`
* Includes built in timer for timeboxing/focused work time

## Usage

Tasks on screen are shown like so:

```
0. Make the bed
1. Complete development project (1:00) Remember to ping Keith on...
2. Get to inbox zero (0:30) http://www.example.com
```

On the left is the **task number**, followed by the **task name**,  the **time spent** on that task so far, if any, and lastly any **note** you left regarding that task. Time spent can be changed manually or can be changed automatically through use of the timer. A green task represents a completed task.

### Commands

|  Key   | Description                                            |
| :----: | ------------------------------------------------------ |
| `[n]`  | Start focus time and timer for task `n`                |
| `a[n]` | (A)dd task at index `n` and notes separated by a colon |
| `c[n]` | Toggle (C)ompletion of task `n`                        |
| `d[n]` | (D)elete task `n`                                      |
|  `dd`  | Delete all tasks                                       |
| `e[n]` | (E)dit task `n`                                        |
|  `h`   | Print the (H)elp menu                                  |
| `m[n]` | (M)ove task `n`                                        |
|  `n`   | Toggle full (N)otes when printing tasks                |
|  `q`   | (Q)uit                                                 |
|  `r`   | (R)educe/remove the completed tasks from the list      |
|  `s`   | (S)tart a new set of daily tasks                       |

### Storage

The default Tod file path is `.tod`. This can be customized in an `.env` file in the root directory of the program:

    TOD_FP={filepath}

### Shell

To reduce the friction of using this every day, I made an alias in my terminal so I can just write `tod` to bring up the program:

`alias tod="python '/Users/your-username/tod_directory/tod.py'"`

Take the above code and copy it into your `~/.bashrc` file. After completing this, run `source ~/.bashrc` for the new changes to be active.

### Future Improvements

* Fix move screen "Move Where" not clearing correctly

* Show notes with title on timer page

* Allow maintaining of title or notes in edit mode (use `:` at start to keep title, use no `:` to keep notes)

* Maybe use `::` to separate to make it not throw in weird ways

* Add ability to count up, not necessarily count down, for time spent

* Add sections for task list, e.g.

  ```ini
  [WORK]
  [ ] Thing to do: yeah
  [X] Other thing
  
  [PROJECTS]
  [ ] Stuff: thing
  
  ...
  ```

  
