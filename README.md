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
    - Manually refresh the Markdown YAML metadata.



## Usage

### How to search?

> **NOTE**: The following `␣` means `Press the Space bar`.

- `s`: **S**earch and open ( if existing ) a new note. All searching method involved is case-insensitive.
    - `s␣`: List recently modified files sorted in reverse order by modification time.
    - `s␣test`: Fast match the title by `keyword` "test"
    - `s␣test␣`: Full text search by `keyword` "test"
    - `s␣test␣alfred`: Full text search by `keyword` "test" and "alfred"
    - `s␣,test`: Full text search by `tag` "test"
    - `s␣k1␣k2,t1␣t2`: Full text search by `keyword`"k1", "k2" and `tag` "t1","t2"
- `sl␣`: Search and show Markdown links contained in the current note which is opened in the front Typora window.
- `sbl␣`: Search and show **Backlinks** related to the current opened note.

### How to process my notes?

Once the desired results are showed in Alfred Filter, you can:

- Press `Enter` to open the file.
- Press `Command+Enter` to select your further actions over the file.
  - Copy Markdown link (`[xxx](./?/xxx.md)`) to clipboard.
  - Refresh file's metadata: 'updated time', 'synonyms' and so on.
  - Delete this file.

### How to create new notes?

- `n␣`: Create **N**ew file by selected templates

### Other operations

- `⌘⌥R`: **R**efresh YAML metadata of the current Markdown file and update all files' "synonyms"&"backlinks" in the background.
- `PKManager Configuration`: Config your preference
  - Set specific config
  - Refresh YAML and update searching cache
  - Open config file
  - Open templates folder
  - Reset all configs to default



## Configuration

- Set Workflow variables

    - `notes_path`: dir of your notes. Only one folder is allowed.
      - It's highly recommended to put all your notes into one folder and give it an unique time ID (e.g. 20200824181348).
      - Check out [this](https://zettelkasten.de/posts/overview/#knowledge-management) blog to learn how to use the method of Zettelkasten to handle your knowledge management.

    - `files_path`: dir of your whole files. It supports multi dirs which include sub-folders.
      - In case you really need multi folders, here is the solution. Use comma `,` to separate your paths.
      - Shallow your folder's depth to enhance searching performance.

    <details>
    <summary>An example setting for the a possible folder tree. ( Click to expand! )</summary>

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



## Dependencies

- [Typora](https://typora.io/): A neat yet powerful Markdown editor with WYSIWYM feature. Highly recommended.
- [Glance](https://github.com/samuelmeuli/glance): All-in-one Quick Look plugin for Mac, which provide perfect preview for Markdown files for dismissing its meta info of YAML frontier.
- Python3: A Python 3 env is needed for some internal scripts, so make sure you've installed it in your env.



## Roadmap

- [ ] Search
    - [ ] Tags auto-completion

    - [ ] Search algorithm: And | Or | Recommendation
    - [ ] Hide / Block files
    - [ ] Preview the first match in filtered result
    - [ ] Improve searching performance
- [ ] Others
    - [ ] Autoupdate: synonyms, backlinks ...
    - [ ] Auto bump version in Workflow by operating info.plist
    - [ ] Notification icon: [yo](https://github.com/sheagcraig/yo)



## Acknowledgement

- Many thanks to the project [`Alfred Markdown Notes`](https://github.com/Acidham/alfred-markdown-notes) ! It's a fantastic workflow but just sadly does not support searching in subdirectories ([ Issue #1](https://github.com/Acidham/alfred-markdown-notes/issues/1#issuecomment-489371014)). Instead of cloning the whole project ( its python code looks too decoupled for me), I decided to partly adopt and refactor its code, which make it much easier to add my own customized features.

- The workflow icon is made by <a href="https://www.flaticon.com/authors/freepik" title="Freepik">Freepik</a> from <a href="https://www.flaticon.com/" title="Flaticon"> www.flaticon.com.</a>
