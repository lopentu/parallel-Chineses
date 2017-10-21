package ntu.ltcl.hanlp;

import java.io.IOException;
import java.util.Map;
import com.sun.net.httpserver.HttpExchange;

import com.hankcs.hanlp.HanLP;
import com.hankcs.hanlp.seg.Segment;
import com.hankcs.hanlp.corpus.tag.Nature;

public class PlaceHandler extends Handler {
  public void handle(HttpExchange httpExchange) throws IOException {
    Map<String,String> params = queryToMap(httpExchange.getRequestURI().getQuery());

    System.out.print("GET:/place ... ");
    System.out.println(params);

    Segment segment = HanLP.newSegment().enablePlaceRecognize(true);
    String places = segmentText(params, segment, Nature.fromString("ns"));

    writeResponse(httpExchange, places);
  }
}
