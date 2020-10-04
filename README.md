# PKManager - Personal Knowledge Manager

A handy **Alfred Workflow** which helps to manage your personal knowledge Markdown notes.



## Main Features:

- Search and open different type of your Markdown files with ease.
    - Notes: Search by title, keywords or tags.
    - Synonyms Redirect: Synonyms is defined in YMAL metadata, which helps to find out the same notes with different keywords.
        - For example, if you create a Note with title `test` and with `synonyms: [tmp, 测试]` in YAML metadata, you can get the exact same note when you search for "test", "tmp" or "测试".
    - Snippets: Search by code's language and keywords
    - Backlinks: To show which note links to the current one. It's an interesting feature motivated by [Roam](https://roamresearch.com/) and [Obsidian](https://obsidian.md/).
        - We use Markdown links `[name](../xx.md)` with a relative path to capture notes' internal connections (and this can avoid syntax issues when using `[[ ]]` ).
        - You can also show every links contained in the current note.
- Create notes with templates
  - Templates: Note, Todo, Snippet, Journal (with location and weather automatically logged)
  - Customized templates are supported.
- Others
    - Auto-update lookups of synonyms, Markdown links, backlinks ...
    - Manually refresh the Markdown YAML metadata.



## Usage

### How to search?

> **NOTE**: The following `␣` means `Press the Space bar`.

- `s`: **S**earch and open ( if existing ) a new note. All searching method involved is case-insensitive.
    - `s␣`: List **RECENT NOTES** sorted in reverse order of modification time.
    - `s␣test`: **TITLE SEARCH** by `keyword` "test"
    - `s␣test␣` / `s␣test␣alfred`: **FULL-TEXT SEARCH** by the **EXACT** `keyword` "test" / `phrase` "test alfred" (case ignored)
    - `s␣test&alfred`: Full-text search by `keyword` "test" **AND** "alfred"
    - `s␣test|alfred`: Full-test search by `keyword` "test" **OR** "alfred"
    - `s␣,t1␣t2|t3&t4`: Full-text search by `tag` "t1" **AND** "t2" **AND** "t3" **AND** "t4" (only the 'and' logic is considered in tag search)
    - `s␣test␣alfred,t1␣t2`: Full-text search by the exact `phrase` "test alfred" and `tag` "t1" and "t2"
- `sl␣`: Search and show **MARKDOWN LINKS** contained in the current note which is opened in the front Typora window.
- `sbl␣`: Search and show **BACKLINKS** related to the current opened note.

### How to process my notes?

- For notes listed in the Alfred Filter as searching results
  - Press `Enter` to open the file.
  - Press `Command+Enter` to select your further actions over the file.
    - Copy Markdown link (`[xxx](./?/xxx.md)`) to clipboard.
    - Refresh file's metadata: 'updated time', 'synonyms' and so on.
    - Delete this file.
- For the note opened in current Typora window
  - `⌘⌥R`: **R**efresh YAML metadata of the current Markdown file

### How to create new notes?

- `n␣`: Create **N**ew file by selected templates

### How to configure preference?

- Set Workflow variables

    - `notes_path`: dir of your notes. Only one folder is allowed.
      - It's highly recommended to put all your notes into one folder and give it a unique time ID (e.g. 20200824181348).
      - Check out [this](https://zettelkasten.de/posts/overview/#knowledge-management) blog to learn how to use the method of Zettelkasten to handle your knowledge management.

    - `files_path`: dir of your whole files. It supports multi directories which include sub-folders.
      - In case you really need multi folders, here is the solution. Use comma `,` to separate your paths.
      - Shallow your folder's depth to enhance searching performance.

    <details>
    <summary>An example setting of a possible folder tree. ( Click to expand! )</summary>

    ```
    ~
    └── Documents/
        └── My_Files/
            ├── Notes/
            │   ├── 20200102030405.md
            │   └── 20200102030522.md
            ├── Archives/
            │   ├── Programming/
            │   └── Ideas/
            ├── images/
            └── Others/
    ```

    ```
    notes_path: ~/Documents/My_Notes/Notes/
    files_path: [~/Documents/My_Notes/Notes/, ~/Documents/My_Notes/Archives/]
    ```
    </details>



- The workflow `PKManager Configuration`: Some operations you can do about customized preferences.

    - `Configure`: Set specific config item
        - `Toggle Modification Monitoring` : Manually/Automatically update notes' lookups of "paths", "synonyms" and "backlinks"
    - `Update Lookups`: Refresh YAML and update searching lookups
    - Open the config file 'Config.json'
    - Open templates folder
    - Reset all configs to default

- Set your templates:

    - Select `Open templates folder` in `PKManger Configuration`. Customize the templates in the folder or place your own template in it.
    - When you type `n_` to create a new file, the workflow will load your templates and update your config automatically.
    - You can modify the default templates, and they'll be restored when you delete any of them.

- Terms explained

    - `metadata`: YAML frontier with important infos placed at the beginning of the Markdown document between two triple dashes. Example:

        ```yaml
        ---
        title: An Example
        synonyms: []
        tags: [test, python]
        typora-root-url: ..
        typora-copy-images-to: ../images
        date: 2020-03-19 04:07:28
        updated: 2020-08-02 14:17:46
        ---

        Content
        ```



## Dependencies

- [Typora](https://typora.io/): A neat yet powerful Markdown editor with WYSIWYM feature. Highly recommended.
- [Glance](https://github.com/samuelmeuli/glance): All-in-one Quick Look plugin for Mac, which provide perfect preview for Markdown files for dismissing its meta info of YAML frontier.
- [fswatch](https://github.com/emcrisostomo/fswatch):  A file change monitor with multiple backends. It's used in auto-updating lookups as you modify your notes, which will improve search performance.
    - Install: `brew install fswatch`
- Python3: A Python 3 env is needed for some internal scripts, so make sure you've installed it in your env.



## Roadmap 🚧

- [ ] Search
    - [ ] Tags auto-completion
    - [ ] Hide / Block files
    - [ ] Preview the first match in filtered result
    - [ ] Improve searching performance
- [ ] Others
    - [ ] Auto bump version in Workflow by operating info.plist
    - [ ] Notification icon: [yo](https://github.com/sheagcraig/yo)



## Acknowledgement

- Many thanks to the project [`Alfred Markdown Notes`](https://github.com/Acidham/alfred-markdown-notes) ! It's a fantastic workflow but just sadly does not support searching in subdirectories ([ Issue #1](https://github.com/Acidham/alfred-markdown-notes/issues/1#issuecomment-489371014)). Instead of cloning the whole project ( its python code looks too decoupled for me), I decided to partly adopt and refactor its code, which make it much easier to add my own customized features.

- The workflow icon is made by <a href="https://www.flaticon.com/authors/freepik" title="Freepik">Freepik</a> from <a href="https://www.flaticon.com/" title="Flaticon"> www.flaticon.com.</a>
