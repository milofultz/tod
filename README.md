# Tod

Plan and manage daily tasks. Deliberately simple so I can stay focused on what I need to do. 
 
* Saves tasks in an easy to read plaintext file in the root folder called `~/.tod`
* Includes built in timer for timeboxing/focused work time 
* Pulls most recent MIT from [Track](https://github.com/milofultz/track) when `s`tarting a new set of daily tasks
* Allows pulling of completed tasks for [Track's](https://github.com/milofultz/track) accomplishment tracking  


### Usage

Tasks on screen are shown like so:

<pre>
0. Make the bed
1. Complete development project (1:00)
2. Get to inbox zero (0:30)
</pre>

On the left is the **task number**, followed by the **task name**, and lastly the **time spent** on that task so far, if any. Time spent can be changed manually or can be changed automatically through use of the timer. A green task represents a completed task.

---

The filepaths for both the Tod tasks file (and the [Track](https://github.com/milofultz/track) file if you use 
[Track](https://github.com/milofultz/track)) should both be in a `.env` file in the root directory of the program. 
The `.env` should use these exact variable names with `{filepath}` being replaced by your desired filepath:

    TOD_FP={filepath}
    TRACK_FP={filepath}
    
---

To reduce the friction of using this every day, I made an alias in my terminal so I can just write `tod` to bring up the program:

`alias tod="python '/Users/your-username/tod_directory/tod.py'"`

Take the above code and copy it into your `~/.bash_profile` file. After completing this, run `source ~/.bash_profile` for the new changes to be active.


### Commands:

* `[n]` - Start focus time and timer for task `n`
* `a[n]` - (A)dd task at index `n`
* `c[n]` - Set (C)ompletion of task `n`
* `d[n]` - (D)elete task `n`
* `dd` - Delete all tasks
* `e[n]` - (E)dit task `n`
* `h` - Print the (H)elp menu
* `m[n]` - (M)ove task `n`
* `q` - (Q)uit
* `r` - (R)educe/remove the completed tasks from the list
* `s` - (S)tart a new set of daily tasks


### Future Improvements

* ~~Add environment variables~~