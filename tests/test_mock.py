import requests
import responses


@responses.activate
def test_simple():
    url = 'http://twitter.com/api/1/foobar'
    responses.add(responses.GET, url, json={'error': 'not found'}, status=404)

    resp = requests.get(url)

    assert resp.json() == {"error": "not found"}

    assert len(responses.calls) == 1
    assert responses.calls[0].request.url == url
    assert responses.calls[0].response.text == '{"error": "not found"}'
