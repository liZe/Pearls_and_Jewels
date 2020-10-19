# python_project_temp
IPI first project in Python + flask


# The idea
Be able to save all funny and WTF moment of our friends / colleagues in a small catchy sentence or image


# HOW TO RUN

use virtualenv
```bash
source flask_api/env/bin/activate
```
then you need to run the react front
```bash
yarn start
```

and the flask api
```bash
yarn start-api
```

and youre up and running !

# Features
- account Creation / Login
- send post (phrase and images)
- react to post (commentary or emote)
- filter and search

# Plus
beautiful UI and ability to style post as we like to match the image / sentence

# Schemas of the tables and their joins

```mermaid!
classDiagram
    Users <|-- Comments
    Users <|-- Pearls
    Pearls <|-- Comments
    Associate <|-- Smileys
    Associate <|-- Pearls
    Associate <|-- Users
    Users : +int id
    Users : +String username
    Users : +String login
    Users : +String psw
    Users: +create()
    Users: +login()
    Users: +update()
    Users: +delete()

    class Comments{
      +int id
      +int id_user
      +int id_pearl
      +String commentaire
      +create()
      +update()
      +delete()
    }
    class Pearls{
      +int id
      +int id_user
      +String content
      +datetime date
      +create()
      +update()
      +delete()
    }
    class Smileys{
      +int id
      +String alt_name
      +String img_link
      +create()
      +delete()
    }
    class Associate{
      +int id
      +int id_users
      +int id_smileys
      +int id_pearls
    }
{
  "theme": "default",
  "themeVariables": {
    "background": "white",
    "primaryColor": "#ECECFF",
    "secondaryColor": "#ffffde",
    "tertiaryColor": "hsl(80, 100%, 96.2745098039%)",
    "primaryBorderColor": "hsl(240, 60%, 86.2745098039%)",
    "secondaryBorderColor": "hsl(60, 60%, 83.5294117647%)",
    "tertiaryBorderColor": "hsl(80, 60%, 86.2745098039%)",
    "primaryTextColor": "#131300",
    "secondaryTextColor": "#000021",
    "tertiaryTextColor": "rgb(9.5000000001, 9.5000000001, 9.5000000001)",
    "lineColor": "#333333",
    "textColor": "#333",
    "mainBkg": "#ECECFF",
    "secondBkg": "#ffffde",
    "border1": "#9370DB",
    "border2": "#aaaa33",
    "arrowheadColor": "#333333",
    "fontFamily": "\"trebuchet ms\", verdana, arial",
    "fontSize": "16px",
    "labelBackground": "#e8e8e8",
    "nodeBkg": "#ECECFF",
    "nodeBorder": "#9370DB",
    "clusterBkg": "#ffffde",
    "clusterBorder": "#aaaa33",
    "defaultLinkColor": "#333333",
    "titleColor": "#333",
    "edgeLabelBackground": "#e8e8e8",
    "actorBorder": "hsl(259.6261682243, 59.7765363128%, 87.9019607843%)",
    "actorBkg": "#ECECFF",
    "actorTextColor": "black",
    "actorLineColor": "grey",
    "signalColor": "#333",
    "signalTextColor": "#333",
    "labelBoxBkgColor": "#ECECFF",
    "labelBoxBorderColor": "hsl(259.6261682243, 59.7765363128%, 87.9019607843%)",
    "labelTextColor": "black",
    "loopTextColor": "black",
    "noteBorderColor": "#aaaa33",
    "noteBkgColor": "#fff5ad",
    "noteTextColor": "black",
    "activationBorderColor": "#666",
    "activationBkgColor": "#f4f4f4",
    "sequenceNumberColor": "white",
    "sectionBkgColor": "rgba(102, 102, 255, 0.49)",
    "altSectionBkgColor": "white",
    "sectionBkgColor2": "#fff400",
    "taskBorderColor": "#534fbc",
    "taskBkgColor": "#8a90dd",
    "taskTextLightColor": "white",
    "taskTextColor": "white",
    "taskTextDarkColor": "black",
    "taskTextOutsideColor": "black",
    "taskTextClickableColor": "#003163",
    "activeTaskBorderColor": "#534fbc",
    "activeTaskBkgColor": "#bfc7ff",
    "gridColor": "lightgrey",
    "doneTaskBkgColor": "lightgrey",
    "doneTaskBorderColor": "grey",
    "critBorderColor": "#ff8888",
    "critBkgColor": "red",
    "todayLineColor": "red",
    "labelColor": "black",
    "errorBkgColor": "#552222",
    "errorTextColor": "#552222",
    "classText": "#131300",
    "fillType0": "#ECECFF",
    "fillType1": "#ffffde",
    "fillType2": "hsl(304, 100%, 96.2745098039%)",
    "fillType3": "hsl(124, 100%, 93.5294117647%)",
    "fillType4": "hsl(176, 100%, 96.2745098039%)",
    "fillType5": "hsl(-4, 100%, 93.5294117647%)",
    "fillType6": "hsl(8, 100%, 96.2745098039%)",
    "fillType7": "hsl(188, 100%, 93.5294117647%)"
  }
}```