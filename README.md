# mjgl-tools

This tool set will allow someone using OBS Studio to dynamically create graphics to display information from the [mahjsoul api](https://github.com/riichinomics/majsoul-api), including:

* The team logos of participants in each match being played in the next session
* The team logos of participants in a selected match within that session
* A graph of scores and current standings as displayed on the [riichi.moe](https://riichi.moe) site

Future features planned for the tool set include:

* Various stats such as riichi rate, dama rate, average hand points value, and more
* 0-4 stats of teams participating in a selected match in the current session
* 0-4 stats of a selected team or player
* Fantasy league points for a selected match in the current session.

## Installation

To install the tool suite, first download a tagged release from the [releases](https://github.com/woogers/mjgl-tools/releases) page. Our release archives also include the MJSL OBS TOOLS directory for convenience. Extract the archive and set configuration options in config.ini using instructions in the Configuration section below.

### Configuration

There are currently five configurable options in config.ini:

#### [config]

* install_path: The absolute filepath to the directory where the MJSL OBS TOOLS directory is located. Default value: `C:\`
* contest_id: The contest id from the api for the contest you wish to grab data for. Default value: `60871d17b5d300559b24998d` (/mjg/ league 2)
* api_url: the url for the api to get data from. Default value: `http://riichi.moe/api`

#### [rankings]

* graph_transparent: Whether or not the generated rankings graph image should be transparent. Default value: `True`
*background_color: The background color of the generated rankings graph image. Accepts [hex color codes](https://www.color-hex.com/) or [names of basic colors](https://matplotlib.org/stable/gallery/color/named_colors.html) (Example: yellow). Default value: `#FFFFFF`

## Usage

Once configuration is complete, execute the tools by launching go.exe. You will be prompted to select which match you wish to get data for.

## Contributing

Pull requests are welcome. For major changes, please open an issue first to discuss what you would like to change. We use [poetry](https://python-poetry.org/) for dependency management.
