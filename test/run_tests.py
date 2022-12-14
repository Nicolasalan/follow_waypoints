import rosunit
import integration_test

# rosunit
rosunit.unitrun('robot_nav', 'integration_test',
                'integration_test.MyTestSuite')