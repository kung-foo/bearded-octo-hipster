angular.module('processListFilters', []).filter('boldFirst', function($sanitize) {
    return function(input) {
        // use $sanitize here because we are _disabling_ the normal sanitizing in the view
        input = $sanitize(input);

        t = input.split(" ", 2);
        p = t[0].split("/");

        bin = p[p.length - 1];

        h = '<span class="bold">' + bin + '</span>';

        if (p.length > 1) {
            h = p.slice(0, p.length - 1).join('/') + '/' + h;
        }

        if (t.length == 2) {
            h += ' ' + t[1];
        }
        return h;
    };
});
