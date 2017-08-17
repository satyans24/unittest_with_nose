import unittest
from sample_tests.sample_api import ProductionClass
from sample_tests.sample_api import API
from mock import patch
from mock import Mock,MagicMock
from nose_parameterized import parameterized
from mock import create_autospec

class SampleTestCase(unittest.TestCase):

    def setUp(self):
        pass

    def tearDown(self):
        pass


    # CASE 1 : Very Basic Test case
    def test_sample_test_case(self):
        p_class = ProductionClass()
        resp = p_class.method('1')
        self.assertEqual(1,resp)



    # CASE 2 : Without mocking function test case
    def test_google_resp_messages(self):
        p_class = ProductionClass()
        resp = p_class.get_goolge_url_status_message()
        #self.assertEqual(resp,"ok", msg="Expected okk but got resp = {0}".format(resp))
        self.assertTrue(resp!="ok",msg="Expected okk but got resp = {0}".format(resp))
        #self.assertIn('temp',['temp'])
        # assertTrue 
        # assertIs
    


    
    # CASE 3: Mocki

    
    
    @patch('sample_tests.sample_api.API.status') # full path from sys.path
    def test_google_resp_messages_new(self,g_api_method):
        p_class = ProductionClass()
        # case 1, 200:

        g_api_method.return_value = 200
        resp = p_class.get_goolge_url_status_message()

        self.assertEqual(resp,"ok")


        g_api_method.return_value = 302
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



    """
    # Case 3: Parameterized
    @parameterized.expand([
        ("OK", 200,"ok"),
        ("REDIRECT", 302,"redirection"),
        ("ERROR", 500,"Error"),
        ("NETWORK", 'Error',"Network"),
        ("NONE", None, "UNKNOWN"),
    ])
    @patch('sample_tests.sample_api.API.status')
    def test_google_resp_messages_new(self, name, input_case, expected, g_api_method):
        p_class = ProductionClass()

        g_api_method.return_value = input_case
        resp = p_class.get_goolge_url_status_message()
        self.assertEqual(resp, expected)

    """
    """

    


    @patch('sample_tests.sample_api.API',spec=API) # relative path
    def test_google_resp_messages_new_auto_spec(self,g_api):
        p_class = ProductionClass()
        # case 1, 200:
        status_fun = MagicMock(return_value=200)
        g_api.status = status_fun
        g_api.status.return_value = 200
        resp = p_class.get_goolge_url_status_message()

        self.assertEqual(resp,"UNKNOWN")
    """

    
    def test_google_resp_messages_new_auto_spec(self):
        p_class = ProductionClass()
        # case 1, 200:
        m_method = create_autospec(API.status,return_value=200)

        #g_api.status.return_value = 200
        resp = p_class.get_goolge_url_status_message()

        self.assertEqual(resp,"ok")



    """
    @patch("sample_tests.sample_api.requests.Response")
    @patch("sample_tests.sample_api.requests")
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
    @patch("sample_tests.sample_api.requests.Response")
    @patch("sample_tests.sample_api.requests")
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
    @patch("sample_tests.sample_api.requests.Response")
    @patch("sample_tests.sample_api.requests")
    def test_get_status_obj_from_requests_side_effect(self,call_type, st_code, r_object,resp_obj):

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

