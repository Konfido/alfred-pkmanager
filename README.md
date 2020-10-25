# Alfred PKManager

A handy **Alfred Workflow** which helps to manage your Personal Knowledge Markdown notes.



## Main Features

- Search
    - Search Notes: Search by title, keywords, tags or synonyms (which need to be predefined in YMAL [metadata](#How to set templates?)).
    - Search Snippets: Search by code's language and keywords
- Show Links and Backlinks
    - Show Links: Show Markdown links contained in the current notes.
    - Show Backlinks: Show which note links to the current one. It's an interesting feature motivated by [Roam](https://roamresearch.com/) and [Obsidian](https://obsidian.md/).
    - **Note**: To avoid syntax issues when using symbol `[[ ]]` in [Typora](https://typora.io), this workflow will search through all the notes for Markdown links ( `[xx](../xx.md)` with a relative path) and use these to process notes' internal connections.
- Create notes with templates
  - Templates: Note, Todo, Snippet, Journal (with location and weather automatically logged)
  - Support customized templates.
- Others
    - Auto-update lookups of synonyms, Markdown links, backlinks ...
    - Manually refresh the Markdown YAML metadata.



## Usage

### How to configure preference?

- First, please set the Workflow variables.

    - `notes_path`: dir of your notes. Only one folder is allowed.

        - It's highly recommended to put all your notes into one folder and give it a unique time ID (e.g. 20200824181348).
        - Check out [this](https://zettelkasten.de/posts/overview/#knowledge-management) blog to learn how to use the method of Zettelkasten to handle your knowledge management.

    - `files_path`: dir of your whole files. It supports multi directories which include sub-folders.

        - In case you really need multi folders, here is the solution. 
        - Use comma `,` to separate your paths.
        - Shallow your folder's depth to enhance searching performance.

    - <details>
        <summary>Example: A possible setting under the following folder tree. ( Click to expand! )</summary>


        ```
        #  An possible setting of your folder tree.
        
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

- Configure in detail through the workflow `PKManager Configuration`

    - `Configure`: Set specific config items
        - `Toggle Modification Monitoring` : Manually **OR** Automatically update notes' lookups of "paths", "synonyms" and "backlinks"?
        - `Toggle Tags Searching Mode`:  Search notes by tags which is specified by metadata "tag" in YAML frontier **OR** by the hash (#) mark in the content?
        - `Toggle Snippet Searching Mode`: Search snippet by code's language specified in code fences **OR** metadata "language" in YAML frontier?
        - `Toggle Order of To-dos`: List the newest **OR** the oldest To-dos in the top?
        - `Toggle Search Scope`: Search Snippet and Notes in its exclusive folder (refer to configs of "path_to_new_xxx") **OR** in all folders?
        - `Number of Reserved Search Results`
        - `Configurate Weather API Key`: Weather API is used to fetch the weather info during creating Journals.
            - Press ⌘ to create your free weather API first.
            - Check out this configuration again and input your your API key.
        - `Desired Path to New xxx`: Set the path to the note/snippet/todo/...
    - `Update Lookups`: Refresh YAML and update searching lookups
    - `Open Config File`: Open the config file "Config.json"
    - `Open Templates Folder`: Open the folder. Revise the Markdown templates or put your own templates files in this folder.
    - `Reset All Configurations`: Reset all settings to default.

### How to preset notes and templates?

- <details>
    <summary>Set the metadata of your notes ( Click to expand! )</summary>


    - `metadata`: A YAML frontier placed at the beginning of the Markdown document between two triple dashes. It defines some important infos which will be used in searching.

    - Example:

        ```yaml
        ---
        title: An Example
        synonyms: [tmp]
        tags: [test, python]
        hidden: False
        typora-root-url: ..
        typora-copy-images-to: ../images
        date: 2020-03-19 04:07:28
        updated: 2020-08-02 14:17:46
        ---
        
        Your note content.
        ```

    - `hidden`: Set to "True" to hide/block specific notes from searching result.

    - `synonyms`: Define a list of synonyms for current note's title, which helps to find out the same notes when using different keywords/abbreviations.

        - Example: If you create a Note with title `test` and with `synonyms: [tmp, 测试]` in YAML metadata, you can get the exact same note when you search for "test", "tmp" or "测试".
            </details>

- Set your templates:

    - Select `Open templates folder` in `PKManger Configuration`. Customize the templates in the folder or place your own template in it.
    - When you type `n_` to create a new file, the workflow will load your templates and update your config automatically.
    - You can modify the default templates, and they'll be restored when you delete any of them.


### How to search?

- `s`: **S**earch and open ( if existing ) a new note. All searching method involved is case-insensitive. ( **NOTE**: The following `␣` means "Press the Space bar". )
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
    - `Back`: Go back to parent menu.
    - `Copy Relative Path`: Copy the relative path of selected note to current opened note (in Typora).
    - `Copy Markdown Link`: Copy Markdown link (`[xxx](./?/xxx.md)`) to clipboard.
    - `Reveal in Finder`: Reveal selected file in Finder.
    - `Delete`: Delete selected file.
- For the note opened in current Typora window
  - `⌘⌥R`: **R**efresh the metadata "Updated" of the current Markdown file

### How to create new notes?

- `n␣`: Create **N**ew file by selected templates



## Dependencies

- Compulsory
    - [Typora](https://typora.io/): A neat and powerful Markdown editor with WYSIWYM feature.
    - Python3: Python 3 is needed for internal scripts, so make sure you've installed it in your env.
- Optional
    - [fswatch](https://github.com/emcrisostomo/fswatch):  A file change monitor with multiple backends. It's used in auto-updating lookups as you modify your notes, which will improve search performance.
        - Install: `brew install fswatch`
    - [Glance](https://github.com/samuelmeuli/glance): All-in-one Quick Look plugin for Mac, which provide perfect preview for Markdown files for dismissing its meta info of YAML frontier.



## Roadmap 🚧

- [ ] Search
    - [ ] Tags auto-completion
    - [ ] Improve searching performance
- [ ] Others
    - [ ] Auto bump version in Workflow by operating info.plist



## Acknowledgement

-  [`Alfred Markdown Notes`](https://github.com/Acidham/alfred-markdown-notes) inspired me to create this workflow to meet my personal need.
- The icon is made by <a href="https://www.flaticon.com/authors/freepik" title="Freepik">Freepik</a> from <a href="https://www.flaticon.com/" title="Flaticon"> www.flaticon.com.</a>

- This workflow is built on the following projects:
    - [CoreLocationCLI](https://github.com/fulldecent/corelocationcli): Command line program to print location information from CoreLocation.
    - [terminal-notifier](https://github.com/julienXX/terminal-notifier): Send User Notifications on macOS from the command-line.