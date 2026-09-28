# GitHub Publishing Workbook

This workbook takes you from the working folder on your Mac to a public GitHub
repository that other people can download and run locally. No previous Git or
GitHub experience is assumed.

## What you are publishing

You are publishing the source code and installation instructions, not your
existing Conda environment or downloaded model files. Each user creates a fresh
local environment by following the repository instructions.

The repository does not need any interview transcripts. Before publishing,
keep research data and participant information outside this project folder.

## Part 1: Check the project locally

1. Open **Terminal**.
2. Move into the project folder:

   ```bash
   cd "/Users/sui/Desktop/Interview transcripts/chinese_segmentation_comparator"
   ```

3. Run the automated tests in the working environment:

   ```bash
   conda run -n chinese-seg38 python -m pytest
   ```

4. Check that all five packages can be imported:

   ```bash
   conda run -n chinese-seg38 python scripts/check_install.py
   ```

5. Start the app:

   ```bash
   bash scripts/run.sh
   ```

6. In the browser, run all five tools on the example text and download a
   comparison report. Return to Terminal and press **Control-C** to stop the app.

Checkpoint: the tests pass, all packages show `[OK]`, and all five tools return
a result.

## Part 2: Create a GitHub account and repository

1. Go to <https://github.com> and create an account, or sign in.
2. In the upper-right corner, select **+**, then **New repository**.
3. Enter a repository name such as `chinese-segmentation-comparator`.
4. Add a short description, for example:

   > Compare Chinese word segmentation from Jieba, HanLP, LTP, pkuseg, and THULAC.

5. Choose **Public** so other people can find and download it.
6. Leave **Add a README file**, **Add .gitignore**, and **Choose a license**
   unchecked. These first two files already exist locally; licensing is covered
   in Part 6.
7. Select **Create repository**.
8. Keep the resulting page open. GitHub displays the repository URL needed in
   Part 4. It will look like:

   ```text
   https://github.com/YOUR-USERNAME/chinese-segmentation-comparator.git
   ```

Checkpoint: GitHub shows an empty repository and its setup instructions.

## Part 3: Turn the local folder into a Git repository

Run these commands in Terminal from the project folder:

```bash
cd "/Users/sui/Desktop/Interview transcripts/chinese_segmentation_comparator"
git init
git branch -M main
git status
```

Read the `git status` list. It should contain application files, tests,
documentation, and scripts. It should not contain `.venv`, `.conda38`, Python
caches, model caches, interview transcripts, or exported result files.

Then create the first saved version:

```bash
git add .
git status
git commit -m "Initial release"
```

If Git asks for your identity, run the following two commands with your own
name and GitHub email, then repeat the commit command:

```bash
git config --global user.name "YOUR NAME"
git config --global user.email "YOUR-GITHUB-EMAIL"
```

Checkpoint: `git status` says the working tree is clean.

## Part 4: Connect and upload to GitHub

Replace the example URL with the URL shown in your empty GitHub repository:

```bash
git remote add origin https://github.com/YOUR-USERNAME/chinese-segmentation-comparator.git
git push -u origin main
```

GitHub may open a browser sign-in window. Complete the sign-in; GitHub no
longer accepts an account password directly in the Terminal password prompt.

Refresh the repository page. You should now see `app.py`, `README.md`,
`environment.yml`, the `segmenters` folder, and the other project files.

Checkpoint: the files appear on GitHub and no private data appears in the file
list or commit history.

## Part 5: Test the instructions as a new user

The most useful release test is a clean installation in a different folder.
Use the repository's green **Code** button to copy its HTTPS URL, then run:

```bash
cd /tmp
git clone https://github.com/YOUR-USERNAME/chinese-segmentation-comparator.git cws-clean-test
cd cws-clean-test
bash scripts/setup.sh
bash scripts/run.sh
```

The setup can take a while. HanLP and LTP also download model data the first
time they are selected. After all five tools work, stop the app with
**Control-C** and remove the temporary test folder:

```bash
cd /tmp
rm -rf cws-clean-test
```

Checkpoint: the app works from the downloaded copy, not only from the original
folder.

## Part 6: Choose a license

A public repository is visible, but without a license other people do not have
clear permission to reuse or modify the code. On the GitHub repository page:

1. Select **Add file**, then **Create new file**.
2. Name the file `LICENSE`.
3. Select **Choose a license template**.
4. A common permissive choice for a small open-source application is the MIT
   License. Review your institution's policy before selecting it, especially if
   this software is part of funded or employed research.
5. Select **Review and submit**, then commit the new file to `main`.

Note that your license covers this application's code. Jieba, HanLP, LTP,
pkuseg, THULAC, their models, and their dependencies retain their own licenses.

## Part 7: Add a release people can cite

Once the clean-install test succeeds:

1. Open the repository on GitHub.
2. Select **Releases**, then **Create a new release**.
3. Select **Choose a tag**, enter `v1.0.0`, and create the tag.
4. Set the title to `Chinese Segmentation Comparator v1.0.0`.
5. Briefly describe the five tools, comparison view, and text exports.
6. Select **Publish release**.

GitHub automatically provides downloadable `.zip` and `.tar.gz` source
archives. You do not need to upload your Conda environment as a package.

## Part 8: Publish later changes

After editing and testing the app, inspect and upload the next version with:

```bash
git status
git diff
git add .
git commit -m "Describe the change briefly"
git push
```

Never use `git add .` until you have read `git status` and confirmed that no
research data, secrets, or large model files are listed.

## Instructions for repository visitors

Visitors with Anaconda or Miniconda installed can run:

```bash
git clone https://github.com/YOUR-USERNAME/chinese-segmentation-comparator.git
cd chinese-segmentation-comparator
bash scripts/setup.sh
bash scripts/run.sh
```

The scripts target macOS and Linux. Windows users should use WSL, because
`pkuseg` 0.0.25 relies on a legacy native build that is difficult to reproduce
in a regular Windows command prompt.

## Troubleshooting

### `conda: command not found`

Install Miniconda or Anaconda, close Terminal completely, reopen it, and rerun
the setup script.

### A path or compiler error mentions `pkuseg`

Do not place the Conda environment inside a path containing spaces. The supplied
script uses the named environment `chinese-seg38`, whose default location does
not contain spaces.

### HanLP reports a chunk-size mismatch

Download its model archive directly, then run the app again:

```bash
mkdir -p ~/.hanlp/tok
curl -fL --retry 5 -o ~/.hanlp/tok/coarse_electra_small_20220616_012050.zip \
  https://file.hankcs.com/hanlp/tok/coarse_electra_small_20220616_012050.zip
```

### Git says `remote origin already exists`

Inspect the existing address:

```bash
git remote -v
```

If it is the wrong repository, replace it:

```bash
git remote set-url origin https://github.com/YOUR-USERNAME/chinese-segmentation-comparator.git
```

### GitHub rejects the push or asks repeatedly for a password

Sign in through the browser prompt, use GitHub Desktop, or configure a GitHub
personal access token. Do not put a token in a project file or commit it.
