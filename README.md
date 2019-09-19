# Vocabulary Backend

> This repository includes the Django project files for the Sanasto app and the build version of the frontend. The frontend source code is in a separate repository in https://github.com/atoivanen/vocabulary-frontend.

## About Sanasto

Sanasto is a web app that helps learning a foreing language. It automatically builds vocabularies from given texts. The current version uses [spaCy](https://spacy.io/) to lemmatize French and Italian texts and [FreeDict's](https://freedict.org/) French-Finnish, French-English, and Italian-Finnish dictionaries to build vocabularies. 

The app has been made as part of the Full Stack Open course of the University of Helsinki. It is not actively developed or maintained.

## Demo

A demo version with limited functionality is running on a hobby server at http://sanasto.herokuapp.com. SpaCy cannot be run on the server because of too little memory. Database is limited to 10 000 rows.

## Built with

- [Django](https://www.djangoproject.com/)
- [React](https://reactjs.org/)
- [PostgreSQL](https://www.postgresql.org/)
- [Django REST framework](https://www.django-rest-framework.org/)
- [spaCy](https://spacy.io/)
- [FreeDict](https://freedict.org/)
- [React Bootstrap](https://react-bootstrap.netlify.com/)
- [axios](https://github.com/axios/axios)
- [i18next](https://www.i18next.com/)
- [React Redux](https://react-redux.js.org/)
- [React Autosuggest](https://react-autosuggest.js.org/)

## License

- [Apache-2.0](https://opensource.org/licenses/Apache-2.0)
- © [Aurora Toivanen](https://fi.linkedin.com/in/aurora-toivanen)