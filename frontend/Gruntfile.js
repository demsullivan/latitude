module.exports = function(grunt) {

  require('load-grunt-tasks')(grunt);

  grunt.initConfig({
    pkg: grunt.file.readJSON('package.json'),

    bower_concat: {
      all: {
        dest: {
          js: 'dist/assets/js/vendor.js',
          css: 'dist/assets/css/vendor.css'
        }
      }
    },

    babel: {
      options: {
        sourceMap: true,
        presets: ['es2015']
      },
      dist: {
        files: {
          'dist/assets/js/latitude.js': 'app/app.js'
        }
      }
    },

    sass: {
      options: { sourceMap: true },
      dist: {
        files: {
          'dist/assets/css/vendor.css': 'build/assets/css/vendor.scss'
          'dist/assets/css/latitude.css': 'src/styles/app.scss'
        }
      }
    }
  });

  grunt.registerTask('default', ['bower_concat', 'babel', 'sass']);
}
