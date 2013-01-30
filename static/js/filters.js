angular.module('processListFilters', []).filter('boldFirst', function($sanitize) {
    return function(input, sep) {
        // use $sanitize here because we are _disabling_ the normal sanitizing in the view
        //input = $sanitize(input);

        //t = input.split(" ", 2);
        p = input[0].split(sep);

        bin = p[p.length - 1];

        h = '<span class="bold">' + bin + '</span>';

        if (p.length > 1) {
            h = p.slice(0, p.length - 1).join(sep) + sep + h;
        }

        if (input.length > 1) {
            h += ' ' + input.slice(1, input.length).join(' ');
        }

        return h;
    };
}).filter('formatSize', function() {
    // from: http://code.google.com/p/jquery-utils/source/browse/trunk/src/jquery.utils.js
    return function(input) {
        var b = parseInt(input, 10);
        var s = ['byte', 'bytes', 'KB', 'MB', 'GB'];
        if (isNaN(b) || b === 0) { return '0 ' + s[0]; }
        if (b == 1)              { return '1 ' + s[0]; }
        if (b < 1024)            { return  b.toFixed(2) + ' ' + s[1]; }
        if (b < 1048576)         { return (b / 1024).toFixed(2) + ' ' + s[2]; }
        if (b < 1073741824)      { return (b / 1048576).toFixed(2) + ' '+ s[3]; }
        else                     { return (b / 1073741824).toFixed(2) + ' '+ s[4]; }
    }
});