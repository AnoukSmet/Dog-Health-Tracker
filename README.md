# **Dog Health Tracker**

## **Goal for this project**

Have you ever gone to the veterinarian with your dog and they ask all kind of questions that you don't really know the answer to...
How much activity does your dog have? Have much does he/she eats? Is her weight stable? 
And on top of this, they tell you that your dog should actually lose some weight... Where to start?

The Dog Health Tracker will make you're life much easier! 
Instead writing down all the information about the activity, food, weigth etc. on paper, you can use DHT to track! 
By adding a daily log on the topics previously mentioned, you can easily track the progress of your dog. 

Next time you go to the veterinarian, you choose nicely the progress you and your dog have made! 
And you will finally be able to answer all those questions they are asking! 

Thank you for visiting my project!  
If you have any feedback or questions, head over to my GitHub contact details and feel free to reach out to me.

--- 

<a></a>

## Table of contents 
* [UX](#ux)
    * [User Goals](#user-goals)
    * [User Stories](#user-stories)
    * [Site Owners Goals](#site-owners-goals)
    * [User Requirements and Expectations](#user-requirements-and-expectations)
        * [Requirements](#requirements)
        * [Expectations](#expectations)
    * [Design Choices](#design-choices)
        * [Fonts](#fonts)
        * [Colors](#colors)
        * [Structure](#structure)
* [Wireframes](#wireframes)
* [Features](#features)
    * [Existing Features](#existing-features)
    * [Features to be implemented](#features-to-be-implemented)
* [Technologies used](#technologies-used)
    * [Languages](#languages)
    * [Libraries and Frameworks](#libraries-and-frameworks)
    * [Tools](#tools)
* [Testing](#testing)
* [Deployment](#deployment)
* [Credits](#credits)
* [Closing Note](#closing-note)

--- 

<a name="ux"></a>

## **UX**

<a></a>

### **User Goals**

* The website has to work well on all kind of devices like mobile phones, tables and desktops.
* I want to have a clear dashboard where I can see all the different logs I have created. 
* The log should appear with the most recent one on top to be relevant. 
* I would like to have the option to add my both dog.
* I want to have a profile for my dog where I can enter information like the name, breed etc. 
* The website has to be easy to use and update
* Visually appealing website

[Back to Top](#table-of-contents)

<a></a>

### **User Stories**

* As a user, I would like to have a personal profile for my dog. 
* As a user, I would like to track activity, food and weigth. 
* As a user, I want to be able to add a log on a daily basis. 
* As a user, I would like to have a dashboard where I can have a good overview. 
* As a user, I want to be able to search on date to get specific data. 
* As a user, I want to be able to add special notes to the log whenever relevant. 
* As a user, I want to be able to add another dog.
* As a user, I want to have the possibility to edit a log when I made a mistake or want to add some info. 
* As a user, I want to have the possibiltiy to delete a log as well when no longer relevant. 
* As a user, I want the website to be easy to use. 
* As a user, I want the process to add a log to be simple to not loose too much time. 

<a></a>

### **User Stories**

* As a user, I would like to be able to pick a category
* As a user, I would like to track my score during the game. 
* As a user, I expect a variety of questions so no questions get repeated.
* As a user, I would like to know the correct answer when answered incorrectly.
* As a user, I expect that the game has a nice visually appealing lay out to be in line with the game.
* As a user of a game, the first impression is very important. 
* As a user you already want to get the happy feeling as of the moment you open the website.
* As a user, I expect all the different pages to be in the same style to make it as a whole.
* As a user I want to learn something new while playing a game. 
* As a user, I want the webiste to be easy to use. I prefer not to have too many buttons or options. 
* As a user, I want some extra information on how to play the game in case I don't understand it. 
* As a user, I want to know where I am in the game, to know how many questions I still have left. 
* As a user, I want to be able to restart the game if I don't like the questions in the category.

<a></a>

### **Site owners Goals**
* To have an appealing website that dog owners use to track their dog.
* To have a great functionality so the user feels like this website helps them in their day-to-day life. 
* To make the website as personal as possible by giving the user the possibility to add information about their dog in the profile.


[Back to Top](#table-of-contents)

<a></a>

### **User Requirements and Expectations**

<a></a>

#### Requirements

* Easy to navigate by using the few buttons
* Appealing dashboard with a functional overview
* Easy way to add a log to the dashboard
* Easy way to add another dog to the profile
* Ability to edit and delete existing logs

<a></a>

#### Expectations

* When you have multiple dogs, it should be easy to navigate between them
* To have a dashboard where all the necessary information is visible
* It should be easy to add another log 
* Personalised profile with information about the dog and an image
* To be able to filter on the logs in order to get specific information

[Back to Top](#table-of-contents)

<a></a>

### **Design Choices**

I have used [Coolors](https://coolors.co/ "Coolors.co") to come up with a color scheme that matches the atmosphere of a Health Tracker.
For this website I have deciced to keep design simple, meaning I opted for a white background color with some light gray for the profile and logs.
I have added some color for the buttons to make the design more visually appealing to the user. 

<a></a>

#### Fonts
In order to find appropriate fonts for my website, I have visited [Google Fonts](https://fonts.google.com/ "Google Fonts") to explore the various options.
For the titles and subtitles, I have used the font [Play](https://fonts.google.com/specimen/Play "Play") 
and for the main text I have used [Cormorant Garamond](https://fonts.google.com/specimen/Cormorant+Garamond "Cormorant Garamond"). 

<a></a>

#### Colors

Like I mentioned before, I have decided to use some colors that fit well with the feeling of a Health Tracker.
Below I will explain more why I choose the various colors and for what I will be using them.

![Color Palette](wireframes/color-palette.png)

* #ffffff: I have decided to keep the background of the overall website white in order give the clean look. I will also use this color as text color for the nav bar and buttons.
* #F5F5F5: This color I will use as a background color for the logs on the dashboard in order to have a small contract versus the white background.
* #D9D9D9: This color I will use as a background color for the profile, to stand out a bit more and to make a clear difference between profile and logs.
* #284B63: This will be the color that I will use for my navigation bar and buttons in order to give a bit of color to the website.
* #000000: I will use the standard black color as my text color in order to keep the simple / clean look. 

I have used a contract checker in order to make sure that the contract is sufficient.
This way my content will be easily readable. 

<a></a>

#### Structure

I have chosen to use [Bootstrap](https://getbootstrap.com/) to create an overall structure for my website. 
Bootstrap provides various elements of CSS and Javascript which is very helpful to keep a good structure on your page. 
As Bootstrap is designed for mobile first, I will be certain that my website functions well on mobile.

[Back to Top](#table-of-contents)

--- 
<a></a>
