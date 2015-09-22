"""djangowind AffilMapper to map the drupal/CAS courses to our local modules

an example response:

    <cas:serviceResponse xmlns:cas='http://www.yale.edu/tp/cas'>
    <cas:authenticationSuccess>
    <cas:user>anders</cas:user>
    <cas:attributes>
    <cas:attraStyle>Jasig</cas:attraStyle>
    <cas:uid>22</cas:uid>
    <cas:mail>anders@columbia.edu</cas:mail>
    <cas:created>1435071681</cas:created>
    <cas:language></cas:language>
    <cas:drupal_roles>authenticated user</cas:drupal_roles>
    <cas:drupal_roles>administrator</cas:drupal_roles>
    <cas:courses>crs-1</cas:courses>
    </cas:attributes>
    </cas:authenticationSuccess>
    </cas:serviceResponse>


From that, that user should be assigned to a module for 'crs-1'.

Djangowind calls `map()` on our class with the user object, and the
list of affils as strings. So the response above would correspond to a
call like:

    map(<User anders>, ['crs-1'])

"""


class CourseMapper(object):
    def map(self, user, affils):
        # now all we have to do is fill this bit in...
        pass
