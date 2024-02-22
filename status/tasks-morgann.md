# momothain, backend server & api lead

## 2/20/24: Backend Django setup

### Backend
```bash
python3 -m venv venv
pip install -r requirements.txt
cd server
FILL OUT THE .env
python manage.py runserver
```


TODO:
- api endpoints to alina

### Frameworks
- Django 
  - API (http endpoints)
  - ORM (database models and interaction)
- MongoDB - Database
- Pydantic - Classes: Data validation / type-checking 



## 2/20/24: Architecture
Frontend - Site: Next.js (Gus, Erik, Robert, Alina)
Pages/Routes
UI: Buttons, Sliders
Gateway: data requirement definitions
API Call: http GET/POST request w/ parameters (user input)
app -> lib -> data.js
/routes, /controllers, /models

Backend Server/API: Python Django (Morgann, Malique, Alec, David, Alina)
API Endpoints
Data Transformation: Algorithm/Logic: 
Generate Image
Use some package?
calc ea pixel?
how to map input to ea pixel (location
Real-time Image Editing (TODO: is this server-side or client/frontend-side??)
Filtering: malique opencv
user input: mouse location, selected parameter
Get Data from Database: MongoDB

In
Ran noise
input data
out
Image r,g,b[][]
pixelation / low resolution! grid, artsy and efficient

NASA data
ext: Image

Topics/Data
Oceans
Climate
Trees
..
Noise



## Next.tsx Coding Standards
Morgann: Next.tsx (React, TypeScript). Since the interaction and generation are real-time, we want to run most stuff client-side which means JavaScript. Probably, we'll make an API call for data at the start and every few minutes, so we can definitely pre-process the data however we want through a backend server at each API call. I'm learning this rn and it seems like the easiest and modern, but lmk about express.js or other options. 

or if we can generate videos or images backend then play or interpolate or interact with them in a simple way for minutes?

Git Branches:
Use local branch (e.g backend, morgann, feature-X), 
Pull from more core branch (e.g. main)
Resolve merge conflicts locally (use your discretion and just ask whoever wrote it if you have a conflicting design decision)
Push your branch to remote
Pull Request to core branch (main) to update it 

Naming Conventions:
root = github-project-kebab-case
root/components/ComponentInPascalCase.tsx
interface ComponentPascalProps {
        children?: ReactNode;
        a: number;
        b-optional?: string;
}

export default function ComponentPascal({ children, a, b = 'hi' } : ComponentPascalProps)  {
        return (
                <div>
                …
                </div>
        )
}
root/app/<more-structure>/page-in-kebab-case.ts
root/styles/<more-structure>/styles-matching-page?
root/types/type-pascal.ts
quense/yup: Dead simple Object schema validation
export const typeSchemaCamel = object({
export type TypePascal = InferType<typeof typeSchemaCamel>;

import { object, string, number, date, InferType } from 'yup';

let userSchema = object({
        name: string().required(),
        age: number().required().positive().integer(),
        email: string().email(),
        website: string().url().nullable(),
        createdOn: date().default(() => new Date()),
});

// parse and assert validity

const user = await userSchema.validate(await fetchUser());

type User = InferType<typeof userSchema>;

 {
name: string;
age: number;
email?: string | undefined
website?: string | null | undefined
createdOn: Date
} 
root/constants.ts 
CONSTANT_UPPER_CASE = … . 



## Core Data Types → Algorithms:
(Image1, Image2) 
Morph Cutting → .mp4
Linear Interpolation → .mp4
Continuous/real-time webcam Image
Filter/fire → Image
"Semi-gross color palette. Animating the building blocks with little squiggles and then adding color / feedback effects." Ref 
float[] (e.g. climate values)

## User Input Types:
Geographic Location
Configurations
Data Source: Choose among our pre-filled Database
Speed / refresh rate 
Static
Query/Topic → "English String"
Click → 
1/0  toggle boolean buttons
(int x, int y, int time)
Geographic Location →
 Coordinates (float latitude, float longitude)
String "description"
Real-time
Mouse Location (int x, int y)
Video .mp4 
Audio .mp3


## Coding Conventions
### Git Branches:
Use local branch (e.g backend, morgann, feature-X), 
Pull from more core branch (e.g. main)
Resolve merge conflicts locally (use your discretion and just ask whoever wrote it if you have a conflicting design decision)
Push your branch to remote
Pull Request to core branch (main) to update it 



## review of alina's visulations/topic/output ideas
https://docs.google.com/document/d/1gcYQGo0ZjbXbko7RR7RnifXmDvDyCpB8QSy4GBBE2-U/edit?disco=AAABGMLrJXQ


## 2/6/24 
### votes on alinas ideas
Morgann:
Physics w/ atoms, colors, forces, magic/etc. gen by data
simple: point-masses (loc, velocity), elastic collisions, 
Evolution one? B/c input is two strings, it could be easy to input any data? and use prev and curr data.

### ideas, IO, data specs
Input:
Configurations
Choose among our datasets
Speed / refresh rate
Physics: collisions, gravity, 
Static
Query/Topic → "English String"
Click → 1/0 = toggle boolean buttons
Location →
 Coordinates, 
String description
Real-time
Video .mp4 
Audio .mp3
