## PKManager - Personal Knowledge Manager

A handy **Alfred Workflow** which helps to manage your personal knowledge Markdown notes. `Typora` is the recommended Markdown editor.

> Note: Working in Process, some content may differ among versions.

### Main Features:

- Search / Open your Markdown notes with ease
    - Search by Wiki's name, keywords, tags or synonyms.
- Create notes with templates
  - Note, Todo, Snippet, Journal
  - Also support customized templates
- Others
    - Manually refresh the Markdown YAML metadata: 'updated time', 'synonyms' and so on.



### Usage
- **NOTE**: `␣` means `Press the space bar`; Adopted searching method is case-insensitive
- `s`: **S**earch and open ( if existing ) or create a new wiki/note.
    - `s␣`: List recent files which are sorted in reverse order by modification time
    - `s␣test`: Fast Match. Only search `Note` by `keyword` "test" of its **title**
    - `s␣test␣`: Search all files by `keyword` "test" of its **content**
    - `s␣test␣alfred`: Search all files by `keyword` "test" and "alfred" of their **contents**
    - `s␣,test`: Search all files by `tag` "test"
    - `s␣k1␣k2,t1␣t2`: Search all files by `keyword`"k1", "k2" and `tag` "t1","t2"
- Once you get the result, you can:
  - Press `Enter` to open the file
  - Press `Command+Enter` to select your further actions on the file
    - Copy inter-link (`[xxx](./?/xxx.md)`) to clipboard
    - Refresh file's metadata
    - Delete this file
- `n␣`: Create **N**ew file by selected templates
- `⌘⌥R`: **R**efresh YAML metadata of the current Markdown file and update `synonyms.json` in the background.
- `PKManager Configuration` Config your preference.
  - Set specific config
  - Open config file
  - Open templates folder
  - Reset all configs to default


### Configuration

- Set Workflow variables

    - `notes_path`: dir of your notes. Only one folder is allowed.
      - It's highly recommended to put all your notes into one folder and give it an unique time ID (e.g. 20200824181348).
      - Check out [this](https://zettelkasten.de/posts/overview/#knowledge-management) blog to learn how to use the method of Zettelkasten to handle your knowledge management.

    - `files_path`: dir of your whole files. It supports multi dirs and sub-folders.
      - In case you really need multi folders, here is the solution. Use comma `,` to separate your paths.
      - Shallow your folder's depth to enhance searching performance.
      - 'full text search' is supported for these folders, while 'fast search' (title matching) is not.

    <details>
    <summary>An example setting for the a possible folder tree. ( Click to expand! )</summary>

    ```
    ~
    └── Documents/
        └── My_Files/
            ├── Notes/
            │   ├── foo.md
            │   └── foo2.md
            ├── Archives/
            │   ├── Programming/
            │   └── Ideas/
            └── Others/
    ```

    ```
    NOTES_PATH: ~/Documents/My_Notes/Notes/
    FILES_PATH: [~/Documents/My_Notes/Notes/, ~/Documents/My_Notes/Archives/, ~/Documents/My_Notes/Others/]
    ```
    </details>

- Customise your configs through workflow of `PKManger Configuration`

    - `template`: A markdown file with formatted content used to generate new notes.

        - Select `Open templates folder` in `PKManger Configuration`. Customize the templates in the folder or place your own template in it.
        - Then, when you type `n_` to create a new file, the workflow will load your template and update your config automatically.
        - The default templates can be restored when you delete any of them.
        - The default path for new file created by these templates is the first path you've listed in the workflow env ``

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

    - `synonyms`: An item defined in metadata which is used to find out the same result in Wiki searching
      - Example: If you create a Wiki with title `test` and with `synonyms: [tmp, 测试]` in metadata, you can get the exact same note when you search for wiki "test", "tmp" or "测试".



### Dependencies

- [Typora](https://typora.io/): A powerful Markdown editor with WYSIWYM feature. Highly recommended.
- [Glance](https://github.com/samuelmeuli/glance): All-in-one Quick Look plugin for Mac, which provide perfect preview for Markdown files for dismissing its meta info of YAML frontier.
- Python 3: A Python 3 env is needed for some internal scripts, so make sure you've installed it in your env.





### Roadmap

- [ ] Search
    - [x] Full-text search
    - [x] Tag search
    - [x] Synonyms redirect
      - [ ] Auto-update data of synonyms
    - [ ] Backlink searching
    - [ ] Snippet Search
    - [ ] Search algorithm: And | Or | Recommendation
    - [ ] Hide / Block files
    - [ ] Preview the first match in filtered result
- [ ] Local storage
    - [x] Preferences
    - [x] Templates
    - [ ] Recent hit
- [ ] Rename current file
  - [ ] update backlinks
- [ ] Others
    - [ ] Autoupdate
    - [ ] Auto bump version in Workflow by operating info.plist
    - [ ] Notification icon: [yo](https://github.com/sheagcraig/yo)







### Acknowledgement

- Many thanks to the project [`Alfred Markdown Notes`](https://github.com/Acidham/alfred-markdown-notes) ! It's a fantastic workflow but just sadly does not support searching in subdirectories ([ Issue #1](https://github.com/Acidham/alfred-markdown-notes/issues/1#issuecomment-489371014)). Instead of cloning the whole project ( its python code looks too decoupled for me), I decided to partly adopt and refactor its code, which make it much easier to accomplish my own customized features.

- The workflow icon is made by <a href="https://www.flaticon.com/authors/freepik" title="Freepik">Freepik</a> from <a href="https://www.flaticon.com/" title="Flaticon"> www.flaticon.com.</a>
