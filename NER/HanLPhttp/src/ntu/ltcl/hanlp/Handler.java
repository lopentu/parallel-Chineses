package ntu.ltcl.hanlp;

import java.io.IOException;
import java.io.OutputStream;

import java.util.List;
import java.util.Map;
import java.util.HashMap;
import java.util.stream.Collectors;

import com.sun.net.httpserver.HttpExchange;
import com.sun.net.httpserver.HttpHandler;

import com.hankcs.hanlp.seg.common.Term;
import com.hankcs.hanlp.corpus.tag.Nature;

public abstract class Handler implements HttpHandler {
  protected static String joinWords(List<Term> termList, Nature nature) {
    return termList.stream()
        .filter(term -> term.nature == nature)
        .map(term -> term.word)
        .collect(Collectors.joining(","));
  }

  protected static void writeResponse(HttpExchange httpExchange, String string) throws IOException {
    byte[] response = string.getBytes();
    httpExchange.sendResponseHeaders(200, response.length);

    OutputStream os = httpExchange.getResponseBody();
    os.write(response);
    os.close();
  }

  protected static Map<String, String> queryToMap(String query) {
    Map<String, String> result = new HashMap<String, String>();
    for (String param : query.split("&")) {
        String pair[] = param.split("=");
        if (pair.length > 1)
            result.put(pair[0], pair[1]);
        else
            result.put(pair[0], "");
    }
    return result;
  }
}
