## PKManager - Personal Knowledge Manager

A Alfred Workflow worked with Typora to handle your personal knowledge base that works on top of Markdown files.

> Note: Working in Process, some content may differ between versions.

### Main Features:

- Search / Open your Markdown notes with ease
    - Search by keywords, tags or wiki's name
- Create notes with templates including Wiki, Note, Todo and the ones created by yourself.
- Others
    - Manually refresh the Markdown YAML metadata



### Usage

- `s`: **S**earch and open ( if existing ) or create a new wiki/note. All searching is case-insensitive.
    - `s␣`: List recent `notes` which sorted in reverse order by modification time
        - `␣` means "Press the space bar"
    - `s␣test`: Search the exact `Wiki` "test"
    - `s␣test␣`: Search all notes with the `keyword` "test"
    - `s␣test␣alfred`: Search all notes with the `keyword` "test" and "alfred"
    - `s␣,test`: Search all notes with the `tag` "test"
    - `s␣k1␣k2,t1␣t2`: Search all notes with the `keyword`"k1", "k2" and the `tag` "t1","t2"
    -
    - Press `Command` to insert inter-link (`[xxx](./?/xxx.md)`) to front application
- `n␣`: Create **N**ew file by selected templates
- `r␣`: **R**efresh meta information in the YAML frontier of the current Markdown file.



### Configuration

- Terms explanation

    - `wiki`: A Wiki for any vital terms/concept (without space in its name), which can be linked to other notes. It's stored as a Markdown file and should be placed in one independent folder.

    - `notes`: Normal Markdown files

    - `template`: A markdown file with formatted content used to generate new notes.

        - Select `Open templates folder` in `PKManger Configuration`. Place your created template in the folder and the workflow will
        - Then, when you type `n_` to create a new file, the workflow will load your template and update your config automatically.
        - The default templates can be restored when you delete any of them.

    - `metadata`: YAML frontier with important infos placed at the beginning of the Markdown document between two triple dashes. Example:

        ```markdown
        ---
        title: {var:wiki}
        synonyms: []
        tags: []
        typora-root-url: ..
        typora-copy-images-to: ../images
        date: {date:yyyy-MM-dd HH:mm:ss}
        updated: {date:yyyy-MM-dd HH:mm:ss}
        ---

        Content
        ```

    - `synonyms`: An item defined in metadata which is used to find out the same result in Wiki searching once the input word is listed in its synonyms. Example: if you create a Wiki naming "test" with `synonyms: [tmp, 测试]`, then you get the same note when search for wiki "test", "tmp" or "测试".

- Set Workflow variables

    - `NOTES_PATH`: folder's path to your notes files. Multi paths and sub-folder is supported, but it goes with the increasing of consuming time. Use comma `,` to separate your paths.

    - `WIKI_PATH`: folder's path to your wiki files. Mutil path is supported, but only setting one path is recommended.

    - A possible variables setting for the following folder tree:

        ```
        ~
        └── Documents/
            └── My_Notes/
                ├── Wiki/
                │   ├── foo.py
                │   └── foo2.py
                ├── Develop/
                │   ├── Programming/
                │   └── Ideas/
                └── Others/
        ```

        ```
        WIKI_PATH: ~/Documents/My_Notes/Wiki/
        NOTES_PATH: [~/Documents/My_Notes/Wiki/, ~/Documents/My_Notes/Develop/, ~/Documents/My_Notes/Others/]
        ```



### Dependencies

- [Typora](https://typora.io/): A powerful Markdown editor with WYSIWYM feature. Highly recommended.
- [Glance](https://github.com/samuelmeuli/glance): All-in-one Quick Look plugin for Mac, which provide perfect preview for Markdown files for dismissing its meta info of YAML frontier.
- Python 3: A Python 3 env is needed for some internal scripts, so make sure you've installed it in your env.





### Roadmap

- [ ] Search
    - [x] Full-text search
    - [x] Tag search
    - [ ] Synonyms redirect
    - [ ] Backlink searching
    - [ ] Snippet Search
    - [ ] Search algorithm: And | Or | Recommendation
    - [ ] Hide / Block files
- [ ] Local storage
    - [x] Preferences
    - [x] Templates
    - [ ] Recent hit
- [ ] Rename current file
  - [ ] update backlinks
- [ ] Others
    - [ ] Autoupdate
    - [ ] Integrated with "Dewey Decimal Classification"
    - [ ] Auto bump version in Workflow by operating info.plist







### Acknowledgement

- Many thanks to the project [`Alfred Markdown Notes`](https://github.com/Acidham/alfred-markdown-notes) ! It's a fantastic workflow but just sadly does not support searching in subdirectories ([ Issue #1](https://github.com/Acidham/alfred-markdown-notes/issues/1#issuecomment-489371014)). Instead of cloning the whole project ( its python code looks too decoupled for me), I decided to partly adopt and refactor its code, which make it much easier to accomplish my own customized features.

- The workflow icon is made by <a href="https://www.flaticon.com/authors/freepik" title="Freepik">Freepik</a> from <a href="https://www.flaticon.com/" title="Flaticon"> www.flaticon.com.</a>
