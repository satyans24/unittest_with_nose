import unittest
from main.sample_api import ProductionClass
from main.sample_api import API
from mock import patch
from mock import Mock,MagicMock
from nose_parameterized import parameterized
from mock import create_autospec

class SampleTestCase(unittest.TestCase):

    def setUp(self):
        """ Use this to do task at the beginning of test cases execution
            Eg. setting up environment or set global objects
        """
        pass

    def tearDown(self):
        """
        use this to clear data/objects created because of tests at end of the execution
        :return:
        """
        pass

    # CASE 1 : Very Basic Test case
    def test_sample_test_case(self):
        """
        This test case is testing method function of ProductionClass.
        """
        p_class = ProductionClass()
        resp = p_class.method('1')
        self.assertEqual(1,resp)

    # CASE 2 : Without mocking function test case
    def test_google_resp_messages(self):
        """
        This test is testing get_goolge_url_status_message 
        function of ProductionClass.This function check the status 
        of an URL and return cutomize message.
        """
        p_class = ProductionClass()
        resp = p_class.get_goolge_url_status_message()
        self.assertTrue(resp!="ok",msg="Expected okk but got resp = {0}".format(resp))
        # Try to use msg to give better visiblity why the test case failed.
        # Whenever we are doing assert on Boolean values, we should always give message.

    # CASE 3: Test case using Mock
    # patch is the decorator from mock, it will mock the object and pass it to the underlying functin.
    # It accepts the full path (sys.path) of the object/method to be mocked.
    @patch('main.sample_api.API.status')
    def test_google_resp_messages_with_mock(self, g_api_method):
        """
        Above test case `test_google_resp_messages` simply call the
        function and return the cutom message by actually invoking the 
        API call to the URL.
        However purpose of the unit test case should be to test the functionality 
        of get_goolge_url_status_message method, not the underlying API.

        In this test case, we mock the `status` method of API class.
        Also to test all scenarios, we assign different return value to this mocked method. 
        This way we don't make the actual API call, but just mock it's behaviour.

        `When to use Mock` 
           - Any method which is making API call, DB call or any other external dependency.

        @params
            -`g_api_method` : Mocked instance of `main.sample_api.API.status`
        """
        p_class = ProductionClass()

        g_api_method.return_value = 200 
        # when `main.sample_api.API.status` will be called in this context, it will return 200
        resp = p_class.get_goolge_url_status_message()
        self.assertEqual(resp,"ok")

        g_api_method.return_value = 302
        # when `main.sample_api.API.status` will be called in this context, it will return 302
        resp = p_class.get_goolge_url_status_message()
        self.assertEqual(resp,"redirection")

        g_api_method.return_value = 500
        resp= p_class.get_goolge_url_status_message()
        self.assertEqual(resp,"Error")

        g_api_method.return_value = "Error"
        resp= p_class.get_goolge_url_status_message()
        self.assertEqual(resp,"Network")

        g_api_method.return_value = None
        resp= p_class.get_goolge_url_status_message()
        self.assertEqual(resp,"UNKNOWN")

    # Case 4: Using Parameterized
    @parameterized.expand([
        ("OK", 200,"ok"),
        ("REDIRECT", 302,"redirection"),
        ("ERROR", 500,"Error"),
        ("NETWORK", 'Error',"Network"),
        ("NONE", None, "UNKNOWN"),
    ])
    @patch('main.sample_api.API.status')
    def test_google_resp_messages_with_parameterised_and_mock(self, name, input_case, expected, g_api_method):
        """
        Parameterized accept lists of iterables(list/tupple),
        it calls the same test case multiple times with value in each iterable as parameters.

        :param name: append `name` to current test case name. First value in iterable.
        :param input_case: input value against which we want to test. Second value in iterable.
        :param expected: expected respone for each test case. Third value in iterable.
        :param g_api_method: Mocked object of `main.sample_api.API.status`

        When we run this test case, it will run 5 times for 5 iterables. in each call 
        values of `name`,`input_case` and `expected` will change.

        This test case serve the same purpose that of `test_google_resp_messages_with_mock`
        """
        p_class = ProductionClass()

        g_api_method.return_value = input_case
        resp = p_class.get_goolge_url_status_message()
        self.assertEqual(resp, expected)

    # Case 5: Using autospec
    @patch('main.sample_api.API', spec=API) # relative path
    def test_google_resp_messages_new_auto_spec(self, g_api):
        """
        Patch in mock has 1 disadvantage that if there is a change in mocked function's parameters, tests will still pass
        but we would almost always want to catch passing incorrect parameters to any function we patch hence using
        `autospec` True gives this advantage, now this test will fail if `status` function's declaration changes in future
        :param g_api: mocked main.sample_api.API class
        """
        p_class = ProductionClass()
        # case 1, 200:
        status_fun = MagicMock(return_value=200)
        g_api.status = status_fun
        g_api.status.return_value = 200
        resp = p_class.get_goolge_url_status_message()

        self.assertEqual(resp,"UNKNOWN")

    
    def test_google_resp_messages_new_auto_spec_another_way(self):
        """
        can also use autospec directly
        :return:
        """
        p_class = ProductionClass()
        # case 1, 200:
        m_method = create_autospec(API.status,return_value=200)

        #g_api.status.return_value = 200
        resp = p_class.get_goolge_url_status_message()

        self.assertEqual(resp,"ok")

    """
    @patch("main.sample_api.requests.Response")
    @patch("main.sample_api.requests")
    def test_get_status_obj_from_requests(self, r_object, resp_obj):
        #r_get.return_value = 200
        #r_post.return_value = 405

        r_object.get.return_value = resp_obj
        r_object.post.return_value = resp_obj
    
        # CASE 1: GET
        resp_obj.status_code = 200
        p_class = ProductionClass()
        resp_g = p_class.get_status_obj_from_requests("GET")
        self.assertEqual(200,resp_g)

        resp_obj.status_code = 405
        resp_p = p_class.get_status_obj_from_requests("POST")
        self.assertEqual(405,resp_p)

        resp_p = p_class.get_status_obj_from_requests("NONE")
        self.assertEqual(404, resp_p)

    """
    """
    @parameterized.expand([
        ("GET", 200),
        ("POST", 405),
        ("NONE", 404),
    ])
    @patch("main.sample_api.requests.Response")
    @patch("main.sample_api.requests")
    def test_get_status_obj_from_requests_params(self,call_type, st_code, r_object,resp_obj):

        r_object.get.return_value = resp_obj
        r_object.post.return_value = resp_obj

        resp_obj.status_code = st_code

        p_class = ProductionClass()
        resp = p_class.get_status_obj_from_requests(call_type)
        self.assertEqual(st_code,resp)
    """

    
    @parameterized.expand([
        ("GET", 200),
        ("POST", 405),
        ("NONE", 404),
    ])
    @patch("main.sample_api.requests.Response")
    @patch("main.sample_api.requests")
    def test_get_status_obj_from_requests_side_effect(self, call_type, st_code, r_object, resp_obj):
        """
        When you cover almost everything in code using mock, you generally remains with "how do I cover the exceptions"
        `side_effect` is 1 of the simplest answer to it.
        in this test, we are intentionally adding `AttributeError` in side_effect property of the mocked function
        which simulates the exact behaviour of exception raise in production and so it covers the exception block
        of your code as well.

        :param call_type: call type is input to underlying function we are testing
        :param st_code: status code to mock with
        :param r_object: mock request object
        :param resp_obj: mock response object
        Also note here, while using multiple patch, the decorators are applied bottom-up and the order of the parameters need to match this.
        Why: this is how python makes the order of execution for this test:
        main.sample_api.requests.Response(main.sample_api.requests(test_get_status_obj_from_requests_side_effect))
        and hence parameters order should be carefully written (bottom-up/reverse of patch)
        """
        r_object.get.return_value = resp_obj
        r_object.post.return_value = resp_obj

        resp_obj.status_code = st_code

        p_class = ProductionClass()
        resp = p_class.get_status_obj_from_requests_side_effect(call_type)
        self.assertEqual(st_code,resp)

        r_object.get.side_effect = AttributeError()
        r_object.post.side_effect = AttributeError()
        p_class = ProductionClass()
        resp = p_class.get_status_obj_from_requests_side_effect(call_type)
        self.assertEqual(404,resp)
        # https://github.com/moengage/segmentation/blob/develop/tests_key_metrics/test_base/test_key_metrics_manager.py#L295

