## PKManager - Personal Knowledge Manager

A Alfred Workflow worked with Typora to handle your personal knowledge base that works on top of Markdown files.



### Main Features:

- Search / Open / Create your files with ease.
- Manually refresh the Markdown YAML metadata
    - updated time 
    - and more



### Usage 

- `n`: Search and open ( if existing ) or create a new node. `␣` means "Press the space bar".
    - `n␣`: List sorted `docs` in reverse order by modification time
    - `n␣test`: Search the exact `Node` "test"
    - `n␣test␣`: Search all docs with the `keyword` "test"
    - `n␣test␣alfred`: Search all docs with the `keyword` "test" and "alfred"
    - `n␣,test`: Search all docs with the `tag` "test"
    - `n␣k1␣k2,t1␣t2`: Search all docs with the `keyword`"k1", "k2" and the `tag` "t1","t2"
    - 
    - Press `Command` to insert inter-link (`[xxx](./?/xxx.md)`) to front application
- `nt`: Refresh meta information in the YAML frontier of the current Markdown file.



### Configuration

- Terms explanation

    - `node`: A pivot/hub/Wiki for any vital terms, actually a Markdown file `node_name.md` , which can be checked or linked to other docs with ease and is placed in an independent folder. 

    - `docs`: Normal Markdown files

    - `template`: A markdown file with formatted content used to generate new nodes/docs. You can make your own template and place it in workflow's subfolder `./templates/`

    - `metadata`: YAML frontier with important infos placed at the beginning of the Markdown document between two triple dashes. Example:

        ```markdown
        ---
        title: {var:node}
        synonyms: []
        tags: []
        typora-root-url: ..
        typora-copy-images-to: ../images
        date: {date:yyyy-MM-dd HH:mm:ss}
        updated: {date:yyyy-MM-dd HH:mm:ss}
        ---
        
        Content
        ```

    - `synonyms`: An item defined in metadata which is used to find out the same result in Node searching once the input word is listed in its synonyms. Example: if you create a Node naming "test" with `synonyms: [tmp, 测试]`, then you get the same doc when search for node "test", "tmp" or "测试".

- Workflow variables

    - `NODES_PATH`: folder's path to your nodes

    - `DOCS_PATH`: folder's path to your docs

    - A possible variables setting for the following folder tree: 

        ```
        ~
        └── Documents/
            └── My_Docs/
                ├── Nodes/
                │   ├── foo.py
                │   └── foo2.py
                ├── Develop/
                │   ├── Programming/
                │   └── Ideas/
                └── Others/
        ```

        ```
        NODES_PATH: ~/Documents/My_Docs/Nodes/
        DOCS_PATH: [~/Documents/My_Docs/Nodes/, ~/Documents/My_Docs/Develop/, ~/Documents/My_Docs/Others/]
        ```



### Dependencies

- [Typora](https://typora.io/): A powerful Markdown editor with WYSIWYM feature. Highly recommended.

- [Glance](https://github.com/samuelmeuli/glance): All-in-one Quick Look plugin for Mac, which provide perfect preview for Markdown files for dismissing its meta info of YAML frontier.





### Roadmap

- [ ] Synonyms redirect

- [ ] Backlink searching

- [ ] Full-text search

- [ ] Tag search

- [ ] Search algorithm: And | Or | Recommendation

    





### Acknowledgement

- Many thanks to the project [`Alfred Markdown Notes`](https://github.com/Acidham/alfred-markdown-notes) ! It's a fantastic workflow but just sadly does not support searching in subdirectories ([ Issue #1](https://github.com/Acidham/alfred-markdown-notes/issues/1#issuecomment-489371014)). Instead of cloning the whole project ( its python code looks too decoupled for me), I decided to partly adopt and refactor its code, which make it much easier to accomplish my own customized features. 

- The workflow icon is made by <a href="https://www.flaticon.com/authors/freepik" title="Freepik">Freepik</a> from <a href="https://www.flaticon.com/" title="Flaticon"> www.flaticon.com.</a>

