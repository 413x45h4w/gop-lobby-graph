import { Page, Section, Text, Callout, Metrics, Table, Grid, Bars, ColumnSeries, Rows, Properties, Segmented, Select, Toggle, Input, Button, TableOfContents, useGrokTheme, useState, useRef, useEffect } from "grok/canvas";
import type { PointerEvent, ReactNode } from "grok/canvas";

const RSA = `
M|John Cornyn|R|S-TX|jd|at|nv|l.88p.jy.y7.au.4q9.3cb.p.i.f0.w.g.ic.0.1.0.7.0.3.2.1
M|J. French Hill|R|H-AR-2|gt|9a|nn|k.8n8.ix.q8.8n.1et.1l8.7.c.bx.k.c.cs.r.1e.c.2.1.11.0.2
M|Ted Cruz|R|S-TX|fx|91|mw|h.7zd.hd.1nt.ap.6my.24d.l.7.if.1c.e.v2.0.1.3.4.0.0.0.3
M|Dan Sullivan|R|S-AK|dm|dr|mh|9.5w2.mt.5xc.8i.83m.u9l.8.7.41.p.d.gq.0.r.1n.4.0.0.0.4
M|Susan M. Collins|R|S-ME|hl|95|mb|c.7kx.q7.2g7.b9.4aw.sxc.p.k.4j.k.c.7o.0.3.2.3.1.2.0.5
M|Andy Barr|R|H-KY-6|g3|d7|ma|v.6gm.mh.sm.94.cbh.6f2.4.2.5j.r.9.9g.t.3.0.3.2.f.1.6
M|Ken Calvert|R|H-CA-41|dz|83|lw|6.c2v.qe.8l.ch.j1.6hn.5.4.v5.m.7.pp.d.0.0.1.3.i.0.7
M|Robert J. Wittman|R|H-VA-1|j5|d5|lv|1f.4sw.g0.gz.7a.wv.8pq.7.4.3n.u.6.gc.h.1a.r.3.4.16.0.8
M|Brian K. Fitzpatrick|R|H-PA-1|9s|c6|lu|1r.3ci.p7.lj.60.1e0.7bz.6.7.6l.e.b.ay.e.0.0.2.4.w.2.9
M|Tom Cole|R|H-OK-4|ib|9d|ls|a.alp.xv.0.ar.ds.0.8.2.193.o.6.1ah.e.6.0.1.2.m.0.a
M|Jacky Rosen|D|S-NV|a2|a2|lg|n.6vr.ko.1zx.bx.72b.kh2.7.1.6d.p.e.vz.0.0.0.4.3.2.1.b
M|Roger F. Wicker|R|S-MS|lb|ae|l1|p.80v.ns.1z.b1.b7.m.j.k.x4.v.g.kb.0.0.0.6.0.1.0.c
M|Tammy Baldwin|D|S-WI|4w|dz|ky|1h.501.i5.68.a7.5ox.lhp.9.7.km.a.8.ew.0.0.0.3.2.0.0.d
M|Deb Fischer|R|S-NE|ly|57|kx|15.52t.m3.jr.8g.ld.5vs.e.a.61.g.a.d0.0.1.0.8.0.5.0.e
M|John R. Curtis|R|S-UT|kn|8c|kw|18.5fl.m2.p.8x.1v1.27.3.1.8g.p.c.42.o.1h.2k.4.4.k.0.f
M|Shelley Moore Capito|R|S-WV|lj|8e|ku|1q.3yc.ox.1j.8c.hz.0.d.5.mq.d.6.9v.0.1d.3u.4.1.4.0.g
M|Bill Hagerty|R|S-TN|co|6m|kr|r.6pv.mj.13h.7x.1be.0.4.3.7q.x.f.2i.0.1.0.5.0.4.2.h
M|Bill Cassidy|R|S-LA|8d|bn|kh|t.6l9.jt.wp.a8.a.f3.m.e.h0.i.9.a6.0.0.0.4.0.5.0.i
M|John Barrasso|R|S-WY|iu|8s|kh|j.8pi.qc.l5.9y.ra.0.7.e.9p.j.b.lw.0.0.0.3.0.1.0.j
M|Marsha Blackburn|R|S-TN|lr|bm|kg|12.5qz.jv.89.8r.av.0.g.4.bf.g.8.7b.0.1.0.5.0.0.1.k
M|Jim Banks|R|S-IN|f0|c9|kf|11.6ac.im.94.8m.34a.0.5.8.5h.j.8.fn.5.3.4.4.1.4.0.l
M|Jason Smith|R|H-MO-8|hs|aj|kc|1.f4q.176.0.ck.47.0.6.5.k4.j.0.os.17.0.0.2.2.q.0.m
M|Tim Scott|R|S-SC|ho|5d|kc|21.3y1.54.6q.5z.2s.0.h.9.ds.r.0.6m.0.b.0.4.1.0.1.n
M|Mark R. Warner|D|S-VA|8o|9d|k8|5.9xi.po.2p2.ey.57.0.e.7.85.s.c.1cw.0.1.1.5.0.8.0.o
M|David G. Valadao|R|H-CA-22|a5|by|k0|20.3ld.ln.42.60.2yb.fzt.6.6.4n.b.2.9a.13.0.0.3.3.8.0.p
M|Christopher A. Coons|D|S-DE|gp|b9|jw|1b.4rk.mq.n1.7t.6r.0.7.a.dn.17.q.ok.0.1.0.5.1.b.0.q
M|Roger Marshall|R|S-KS|ix|ev|ju|1s.3so.kq.9j.5u.25c.10j9.6.6.fe.8.6.1o.0.0.0.4.0.1.0.r
M|Ruben Gallego|D|S-AZ|8i|d3|js|s.739.e3.lv.e1.j8z.fmf.3.6.4h.h.9.nu.4.0.0.5.3.0.0.s
M|Kevin Hern|R|H-OK-1|j6|8v|js|1a.5cq.mm.2h.6y.21d.0.2.4.50.c.4.cr.13.2g.6s.1.3.j.0.t
M|Earl L. "Buddy" Carter|R|H-GA-1|bw|a6|jm|2m.30u.jo.2x.5x.0.dl.5.9.cn.e.0.5t.w.2.0.2.5.k.0.u
M|Steve Scalise|R|H-LA-1|h6|ag|jl|3.drv.lw.6s.7f.0.0.f.f.9o.f.9.1af.31.0.0.0.2.1a.0.v
M|Michael Lawler|R|H-NY-17|ft|ci|jk|2j.2ux.k1.b2.5w.4l1.9sg.0.2.ak.v.a.d0.t.0.0.2.3.p.1.w
M|Tom Cotton|R|S-AR|hv|ea|jg|1v.3dl.d3.tn.5k.gf.0.9.3.a1.q.c.gu.0.0.0.4.1.0.0.x
M|Edward J. Markey|D|S-MA|8l|b7|j9|2l.2dl.5w.14i.4o.17.2m7.7.6.dp.d.8.4g.0.0.0.4.0.0.0.y
M|Mariannette Miller-Meeks|R|H-IA-1|k7|et|j3|2a.30t.wl.3z.5v.2d7.9d0.2.4.jc.4.4.7u.18.0.0.2.3.16.1.z
M|Thom Tillis|R|S-NC|ii|9i|j2|m.8ue.it.5b.9z.y.0.c.c.ay.p.8.cs.0.0.0.5.0.7.0.10
M|Tim Kaine|D|S-VA|9z|7f|iz|i.7af.j1.293.ck.1f.0.4.f.9b.v.r.1e5.0.0.0.4.0.2.0.11
M|Martin Heinrich|D|S-NM|ch|aa|iw|d.a3g.nt.0.db.g.4j.6.8.df.b.7.100.0.1.0.4.0.1.0.12
M|Brett Guthrie|R|H-KY-2|i1|ch|iw|4.clm.1i7.g7.e6.28.0.5.5.97.b.6.kk.23.0.0.1.3.15.0.13
M|Steve Womack|R|H-AR-3|jj|b5|iw|24.3vm.e0.1.6i.4g.4.9.7.l5.e.8.ay.7.0.0.1.2.n.0.14
M|Bill Huizenga|R|H-MI-4|d1|gt|iw|4m.21w.gf.17.3o.1vx.8xc.3.8.5d.l.a.3y.j.0.0.2.2.1q.0.15
M|Steven Horsford|D|H-NV-4|69|dn|iu|1p.41v.mi.17.8q.3hp.2g.9.2.24.c.a.kv.k.0.0.1.5.6.0.16
M|Tom Emmer|R|H-MN-6|kp|bk|iu|8.az1.xb.lf.9h.7j.0.6.7.1k.k.9.k8.2j.0.0.1.4.1c.1.17
M|Richard Hudson|R|H-NC-9|79|eu|it|16.5d6.tx.8.74.1.a6.3.9.6u.c.5.c8.m.0.0.1.1.a.0.18
M|Todd Young|R|S-IN|ei|d9|is|29.3g9.bg.eg.5x.4i.0.f.3.86.v.f.8e.0.0.0.4.0.0.0.19
M|Bryan Steil|R|H-WI-1|7p|7w|is|2u.2th.ko.52.56.3rh.4q2.1.4.58.f.6.3e.w.2.0.4.4.1.0.1a
M|David McCormick|R|S-PA|fy|e6|iq|17.4w4.h5.sa.7z.bwe.1o72.4.0.3r.d.9.5m.0.2.2.5.0.4.0.1b
M|Juan Ciscomani|R|H-AZ-6|fn|e7|ip|3z.23f.jp.73.4c.4y3.cp6.2.3.gu.a.2.7j.p.0.0.2.5.0.1.1c
M|Haley M. Stevens|D|H-MI-11|6y|4w|io|1u.46c.c3.24.9n.q69.uc.2.5.3r.f.7.ac.b.0.0.3.2.6.0.1d
M|Young Kim|R|H-CA-40|e2|bt|io|2o.30e.hu.4x.4x.3e7.5op.2.0.4y.11.9.ei.w.0.0.3.3.i.0.1e
M|Jimmy Panetta|D|H-CA-19|dn|82|in|3c.2l0.hu.0.62.l7.0.3.6.5q.l.e.6g.y.1.0.2.5.o.0.1f
M|Mike Johnson|R|H-LA-4|g7|as|in|2.chl.xf.1zk.82.0.kv.7.8.19.i.0.wb.3q.0.0.0.3.1.0.1g
M|Adrian Smith|R|H-NE-3|jq|cj|im|2k.394.gq.0.54.8a.0.6.4.97.i.0.87.o.0.0.2.2.1k.0.1h
M|Mike Rounds|R|S-SD|hk|fs|il|30.2w1.h2.w.4t.mp.wz.7.6.4q.t.e.2n.0.0.0.6.0.1.0.1i
M|John R. Carter|R|H-TX-31|ml|f1|ii|31.2xx.7a.7x.3x.2b.0.b.6.ke.j.0.6w.4.0.0.1.3.1.1.1j
M|Jerry Moran|R|S-KS|hf|dr|ie|2w.39s.8b.c.4s.0.0.9.b.hj.i.8.2g.0.b.k.6.0.6.1.1k
M|Elissa Slotkin|D|S-MI|8t|87|ib|1m.4j1.4l.bz.9z.j21.gpk.2.4.2o.o.c.dt.1.1.0.4.2.0.0.1l
M|Frank Pallone, Jr.|D|H-NJ-6|9v|9x|i9|b.a4m.vz.0.9j.0.0.9.2.4n.b.5.br.1s.7.0.1.3.r.0.1m
M|August Pfluger|R|H-TX-11|oh|a9|i8|23.39m.c2.o3.5m.47.0.2.2.6i.k.7.6m.1e.3.3.2.2.8.1.1n
M|John Thune|R|S-SD|io|c2|i8|g.9qm.bs.5p.9t.0.0.f.b.7p.p.c.eh.0.0.0.4.0.2.0.1o
M|John Boozman|R|S-AR|f4|6d|i7|2f.3gv.6i.7v.4o.0.0.h.7.8l.g.e.73.0.1n.4e.6.0.5.0.1p
M|Rick Scott|R|S-FL|d0|42|i6|3j.1ti.9j.wg.37.13c.fg.4.2.7s.z.0.em.0.0.0.5.0.0.1.1q
M|Doris O. Matsui|D|H-CA-7|9b|dk|i3|2q.33t.hp.b.4v.3o.gm.8.9.4x.8.3.98.10.0.0.1.3.0.0.1r
M|Blake D. Moore|R|H-UT-1|gm|ab|i3|2p.36f.fd.6.51.ec.dj.2.2.5n.f.0.6o.y.a.p.2.3.6.0.1s
M|Josh Gottheimer|D|H-NJ-5|cp|b1|hx|5d.1rv.dl.p.3m.kz.0.b.7.5g.b.6.8s.4.3m.m4.2.6.0.0.1t
M|Jodey C. Arrington|R|H-TX-19|hi|bk|hw|2t.31n.ck.70.5e.g.0.7.a.251.b.6.52.l.0.0.3.2.7.0.1u
M|Terri A. Sewell|D|H-AL-7|3m|cf|hw|3p.2a9.mf.0.5k.5y.0.5.5.5g.c.b.6a.u.3.0.3.3.1o.0.1v
M|David P. Joyce|R|H-OH-14|j9|6c|hv|2y.2yq.gv.1.5n.26.0.1.8.jm.f.0.7u.j.h.2.2.5.z.0.1w
M|Chris Pappas|D|H-NH-1|9t|dc|ht|22.3uj.ac.4y.7z.2aw.fgk.3.1.34.c.6.eq.c.1.0.2.0.0.0.1x
M|Gus M. Bilirakis|R|H-FL-12|qc|4m|hs|43.2b8.fu.9.4g.kj.0.5.6.bn.f.6.6u.8.0.0.2.4.7.0.1y
M|Gary C. Peters|D|S-MI|i5|6t|hp|36.2z2.6j.17.52.0.0.e.7.ap.l.9.h8.0.f.d.4.0.b.0.1z
M|Robert E. Latta|R|H-OH-5|lh|fv|hp|40.2b9.hl.6.4q.1r.0.b.6.4s.d.5.3r.x.4.0.1.2.1a.0.20
M|Dan Newhouse|R|H-WA-4|l0|64|ho|3q.2kr.b5.a.4j.fu.5d.3.7.3i.b.2.3w.10.15.2l.3.4.j.0.21
M|Julia Letlow|R|H-LA-5|hb|4s|hn|1e.55w.fs.b6.7s.aqi.jj.1.2.1o.a.4.b6.y.o.15.2.3.g.0.22
M|Maria Cantwell|D|S-WA|b4|8v|hm|o.8v3.n.8d.dn.4.0.c.c.id.9.6.xw.0.0.0.6.0.8.0.23
M|Pete Ricketts|R|S-NE|ku|c4|hk|25.3e4.k7.ac.60.13h.ifh.1.0.3c.m.i.d8.0.a.a.4.0.7.0.24
M|Mike Thompson|D|H-CA-4|jt|e4|hk|2r.33m.hv.9.5c.26s.38e.7.3.4d.8.0.5m.3.0.0.1.2.0.1.25
M|Ben Ray Luján|D|S-NM|aw|al|hj|10.5s5.gb.wf.90.7m.0.7.4.6i.a.5.fa.0.0.0.6.1.0.0.26
M|Jack Reed|D|S-RI|gz|5u|hh|28.3vy.bx.1.58.0.0.9.9.s0.m.a.5i.0.0.0.4.0.c.0.27
M|Raja Krishnamoorthi|D|H-IL-8|83|f3|hh|3l.2rd.7f.0.4l.bg.1jt.8.2.2x.a.7.47.k.1.0.3.2.1.0.28
M|Don Bacon|R|H-NE-2|jy|co|hf|6u.1a7.c1.1i.3g.26k.5lm.1.6.38.p.9.4b.1e.0.0.2.5.16.2.29
M|David Schweikert|R|H-AZ-1|im|g1|hf|48.2ak.ck.1i.56.lj.8by.6.8.46.8.2.7d.c.0.0.2.6.0.0.2a
M|Darin LaHood|R|H-IL-16|h3|9n|he|u.5sr.s5.1eo.73.f.0.1.3.68.l.8.gd.n.8.0.3.1.n.0.2b
M|Mario Diaz-Balart|R|H-FL-26|ey|51|he|1j.50b.gs.0.5v.0.0.6.2.74.j.c.f9.l.1.0.1.5.d.0.2c
M|Cindy Hyde-Smith|R|S-MS|dy|gv|hd|2x.2wi.c5.8r.4y.ld.4tw.4.4.ar.7.5.69.0.0.0.5.0.1.0.2d
M|Ron Wyden|D|S-OR|g2|6c|hc|2s.3es.6k.d.5a.0.0.i.a.bn.a.a.al.0.8.9.5.0.8.0.2e
M|Adam B. Schiff|D|S-CA|59|bq|hc|2b.3vt.3n.y.85.5c.0.2.9.61.c.9.n7.b.1.1.4.1.1.0.2f
M|Sam Graves|R|H-MO-6|ji|63|ha|2n.36j.gx.0.6j.0.0.6.8.ss.g.0.58.j.0.0.2.1.j.0.2g
M|Hakeem S. Jeffries|D|H-NY-8|94|a6|h9|f.8ms.tl.w9.ad.6.es.4.7.3.i.h.2bu.1h.1.0.0.5.k.0.2h
M|Joni Ernst|R|S-IA|jm|d0|h9|4c.26l.9v.6t.4q.a.f.l.h.6n.o.b.20.0.0.0.4.0.6.1.2i
M|Michael R. Turner|R|H-OH-10|h7|d2|h3|6q.1g7.6q.1v.23.ig.4ju.9.3.29.p.a.w.m.0.0.2.3.17.0.2j
M|Thomas H. Kean, Jr.|R|H-NJ-7|lj|cq|h2|4n.1zz.cy.55.3v.fq.3qu.0.1.3m.m.6.9p.q.12.1d.2.2.1b.1.2k
M|John Joyce|R|H-PA-13|fi|ex|h2|27.3lt.l7.x.5f.6y.0.5.1.bv.a.0.2u.i.0.0.1.0.1t.0.2l
M|Mike Crapo|R|S-ID|lo|8k|h0|1i.439.am.15w.4m.0.0.g.b.56.d.6.4b.0.0.0.4.0.7.1.2m
M|Tim Sheehy|R|S-MT|ff|ek|gx|14.5rr.bh.7v.8t.d7b.1dr3.0.1.3r.d.3.he.0.3.0.3.0.0.0.2n
M|Andrew R. Garbarino|R|H-NY-2|fb|7j|gw|1z.366.lf.n9.6p.99.g.4.2.4i.6.5.92.1r.2.1.3.3.z.0.2o
M|Robert B. Aderholt|R|H-AL-4|kl|5w|gu|5n.1ta.7f.21.2u.0.0.8.3.j4.f.9.48.j.i.0.1.1.b.0.2p
M|David Rouzer|R|H-NC-7|io|6h|gt|2e.3h2.et.1.4w.47.3.4.5.2y.f.4.79.c.6.2.3.3.6.0.2q
M|Beth Van Duyne|R|H-TX-24|mc|60|gr|3b.2ld.e8.3m.4m.16.21.1.3.5o.d.6.46.o.1.0.2.3.n.3.2r
M|Charles J. "Chuck" Fleischmann|R|H-TN-3|mi|dj|gp|2c.3no.ao.0.5t.0.0.7.2.f4.h.3.a0.b.0.0.2.4.c.0.2s
M|Gregory F. Murphy|R|H-NC-3|7c|4m|go|4r.23q.c4.c.46.pk.9d.5.0.9p.c.4.2k.e.0.0.4.2.j.0.2t
M|James E. Risch|R|S-ID|oa|aq|go|4j.26g.dk.2.40.9.25.7.7.3w.13.k.fb.0.1.0.6.0.0.1.2u
M|Thomas R. Suozzi|D|H-NY-3|9e|be|gn|44.2ff.bn.1.72.3nk.67k.1.7.1h.f.6.81.9.e.2.2.2.1e.0.2v
M|Virginia Foxx|R|H-NC-5|jf|5g|gi|6l.1fk.9s.0.3g.0.9g.6.7.6p.8.4.av.w.8.d.3.2.3.0.2w
M|Ritchie Torres|D|H-NY-15|7z|7a|gg|5g.1rp.6v.6w.34.379.0.2.5.3n.e.0.2w.e.d.i.2.6.7.0.2x
M|Angie Craig|D|H-MN-2|cd|bm|gf|1t.43y.hr.9.9u.8qr.1sb.1.4.1q.8.4.b0.e.0.0.1.2.0.1.2y
M|Bradley Scott Schneider|D|H-IL-10|2q|75|gd|4y.1uj.ib.0.4o.b.r.3.6.6n.p.8.4s.10.1.0.2.3.0.0.2z
M|Brian Schatz|D|S-HI|6i|9v|gc|4e.2f7.7p.0.43.0.0.a.6.iy.o.i.db.0.0.0.5.1.0.0.30
M|Carol D. Miller|R|H-WV-1|ds|7d|gb|2v.32f.g3.0.67.c.1.3.6.5d.c.0.2n.g.y.c.1.1.k.0.31
M|Lisa Blunt Rochester|D|S-DE|90|9b|gb|z.6un.ko.2a.b9.e.0.4.7.4q.c.5.te.7.0.0.4.3.0.0.32
M|John W. Hickenlooper|D|S-CO|93|an|gb|1x.3sj.9x.ec.5o.e8.0.1.2.6q.a.6.go.0.a.g.4.0.0.0.33
M|Ann Wagner|R|H-MO-2|r7|29|gb|58.1rl.eo.1o.38.15.4b.6.3.4g.p.4.4e.8.0.0.2.2.1g.1.34
M|Joseph D. Morelle|D|H-NY-25|6s|5y|g8|3k.27d.a6.hb.59.re.0.2.3.1q.e.5.7d.g.1.0.4.3.2.2.35
M|Bernie Moreno|R|S-OH|fr|d8|g8|1w.3oh.7w.nt.6r.19ck.1txq.0.2.2u.c.3.a1.0.0.0.5.0.4.1.36
M|Ted Budd|R|S-NC|m6|cm|g8|26.3tm.6a.81.68.0.0.7.6.62.i.g.51.0.0.0.5.2.6.0.37
M|Mike Lee|R|S-UT|fq|7l|g7|5p.1y9.3g.0.3q.2s.0.6.e.bn.i.b.8z.0.0.0.4.0.1.0.38
M|Jeanne Shaheen|D|S-NH|lg|77|g6|50.294.3n.0.4x.0.0.b.8.gw.r.q.al.0.0.0.6.1.6.0.39
M|Susie Lee|D|H-NV-3|5u|ge|g4|5w.1q4.9k.1.58.1jl.af.3.5.4t.a.0.2m.f.a.b.2.3.5.0.3a
M|Mike Carey|R|H-OH-15|dd|e9|g4|19.4yh.ni.g5.8f.1dr.31y.0.3.4n.6.3.d9.e.0.0.4.1.7.0.3b
M|Scott H. Peters|D|H-CA-50|dj|3x|g3|41.27e.k2.1j.4n.2n.0.6.6.5o.9.1.50.g.3.2.2.4.n.0.3c
M|Steve Daines|R|S-MT|m1|6l|g3|1k.51y.dc.4.6f.0.0.3.4.9i.k.g.b0.0.1.0.4.0.0.0.3d
M|Lisa Murkowski|R|S-AK|5a|f5|g1|4p.2bb.51.2.50.d.0.j.c.ei.d.4.6q.0.0.0.4.1.1.0.3e
M|Robert Menendez|D|H-NJ-8|f3|bv|g1|1y.46t.87.0.90.1cn.cq.5.4.17.b.6.5k.6.1.0.1.3.l.0.3f
M|Maria Elvira Salazar|R|H-FL-27|c1|4v|fz|8n.ym.6t.2a.1x.3z.1tm.1.5.5f.j.g.9j.x.b.j.2.3.7.0.3g
M|Patty Murray|D|S-WA|8x|4o|fz|3u.2ov.6l.j.4x.0.0.k.i.cj.b.9.ai.0.0.0.4.0.2.0.3h
M|Zoe Lofgren|D|H-CA-18|70|8d|fz|6k.1jt.5t.g.2q.8j.0.7.3.31.a.4.1q.14.1n.1r.2.3.0.0.3i
M|Lisa C. McClain|R|H-MI-9|hq|bx|fz|4s.21b.cx.1q.3t.48.0.2.1.3w.j.9.4e.19.1c.46.2.2.4.0.3j
M|Kathy Castor|D|H-FL-14|9l|fj|fx|4z.21g.b9.2.4a.35y.abf.2.8.37.9.5.3s.6.0.0.2.1.e.0.3k
M|Linda T. Sánchez|D|H-CA-38|aw|ca|fw|34.2yu.a2.0.3i.8c.0.7.5.22.a.6.1y.h.0.0.1.5.j.0.3l
M|Kirsten E. Gillibrand|D|S-NY|6e|5x|fw|4q.1t8.64.gw.2m.t.0.f.e.72.b.b.8m.0.0.0.4.1.2.0.3m
M|H. Morgan Griffith|R|H-VA-9|mo|h2|fw|2z.2zy.ea.0.4p.3.4.6.4.5w.8.3.3k.m.0.0.4.1.2.1.3n
M|Ashley Hinson|R|H-IA-2|ky|e1|ft|13.5ie.gg.hj.84.92.t.3.1.3w.8.4.f7.d.0.0.3.1.0.0.3o
M|Mike Rogers|R|H-AL-3|j1|5b|fs|q.89f.dc.0.ba.0.0.0.3.16t.r.0.ja.7.0.0.1.2.g.0.3p
M|Zachary Nunn|R|H-IA-3|ex|dh|fp|3v.27o.hi.66.4a.2ib.83w.2.1.5k.0.c.0.g.0.0.3.1.0.0.3q
M|Mike Bost|R|H-IL-12|c1|3r|fo|5o.1m5.g8.1.3o.32.k.2.4.4m.b.2.3c.p.3.0.3.4.1p.3.3r
M|Mark Kelly|D|S-AZ|9x|ao|fo|32.38t.o.1g.3j.1r.0.3.3.74.p.a.eq.0.0.0.5.0.1.0.3s
M|Elise M. Stefanik|R|H-NY-21|j4|4p|fn|5z.1ig.82.85.2s.0.0.5.4.6t.o.9.1j.1b.0.0.3.4.a.1.3t
M|Pete Aguilar|D|H-CA-33|bo|9q|fm|x.69h.wr.ed.bg.e8.0.3.3.e.g.6.wu.y.0.0.1.4.0.0.3u
M|Gregory W. Meeks|D|H-NY-5|89|8d|fl|4o.1se.dg.an.37.1a.0.5.9.1v.19.q.lz.y.0.0.2.6.1w.0.3v
M|Christopher Murphy|D|S-CT|hy|g5|fl|5a.274.-2.m.51.0.0.8.a.7l.t.h.aw.0.1.0.3.0.2.0.3w
M|Laurel M. Lee|R|H-FL-15|hw|69|fl|38.2jr.b5.9w.5q.6z.0.1.4.3o.6.0.by.u.f.0.3.2.1.1.3x
M|Eric Schmitt|R|S-MO|lx|cy|fj|1d.5gl.5v.bp.7f.32.0.5.0.3p.d.9.ca.0.0.0.4.0.3.0.3y
M|Sheldon Whitehouse|D|S-RI|i9|c9|fh|4v.1w8.5e.cn.45.0.5.9.8.76.7.6.61.0.z.2o.6.0.1.0.3z
M|Brian J. Mast|R|H-FL-21|i7|4t|fh|8i.13y.4u.k.2j.ee.2d.6.2.3v.18.g.7g.o.1.2.2.4.l.0.40
M|Claudia Tenney|R|H-NY-24|fu|fy|fh|2d.3i4.ef.15.5h.0.0.3.4.6n.d.7.7s.j.0.0.3.1.19.0.41
M|Bruce Westerman|R|H-AR-4|k8|75|fg|3x.28e.is.3h.5k.0.0.5.4.cq.4.4.9u.1d.8.h.2.4.s.0.42
M|Mitch McConnell|R|S-KY|6z|7c|fg|60.1w6.28.0.2z.0.0.v.j.fg.d.c.7j.0.1.f.5.0.6.0.43
M|Cynthia M. Lummis|R|S-WY|nf|du|fe|45.2dd.6o.6m.43.3l.0.7.4.6e.9.2.5u.0.0.0.3.1.0.1.44
M|Margaret Wood Hassan|D|S-NH|bt|da|fd|1l.4qu.b7.0.77.1a.0.4.2.a4.7.7.cy.0.0.0.5.0.b.0.45
M|Andy Kim|D|S-NJ|4q|b6|fd|3a.2zx.2i.s.5w.5o.91.1.6.2r.s.5.ek.2.0.0.5.2.0.0.46
M|Rosa L. DeLauro|D|H-CT-3|ca|3y|fd|3n.2oi.7u.l.5e.0.0.9.4.3w.d.4.9q.f.1.0.1.2.i.0.47
M|Debbie Wasserman Schultz|D|H-FL-25|4p|bp|fc|4k.2c2.7u.0.42.8i.2v.8.6.2o.6.4.eo.9.0.0.2.1.1.1.48
M|John James|R|H-MI-10|md|6s|fa|9z.kp.80.62.2d.ks.5i1.0.4.6p.j.i.hy.f.n.16.1.2.7.0.49
M|Harold Rogers|R|H-KY-5|jn|3v|fa|4h.2f2.65.0.3w.0.0.7.5.gd.h.0.74.4.0.0.1.0.7.0.4a
M|Henry Cuellar|D|H-TX-28|eq|fr|fa|42.2hc.aj.3.3w.7d.5l.8.7.d.b.8.9c.3.0.0.1.2.q.b.4b
M|Jeff Merkley|D|S-OR|7n|8z|f9|67.1rg.57.1.2p.0.0.a.7.l9.l.c.i.0.0.0.6.0.2.0.4c
M|Darrell Issa|R|H-CA-48|o0|e3|f8|4t.283.79.5.39.4.0.6.1.75.r.e.92.8.0.0.3.4.o.0.4d
M|Michael K. Simpson|R|H-ID-2|mg|b8|f7|2h.3ik.9s.3.62.0.0.1.3.gg.d.2.6q.a.5.5.1.3.0.0.4e
M|Diana DeGette|D|H-CO-1|hh|6w|f6|5e.1tm.c5.0.3z.199.5x.6.e.1x.8.4.2e.a.0.0.1.2.l.0.4f
M|David Kustoff|R|H-TN-8|jw|2s|f4|56.1wd.c1.0.3q.0.0.4.3.42.d.5.8r.7.c.0.1.1.16.3.4g
M|Suzan K. DelBene|D|H-WA-1|7x|66|f3|35.2m5.j8.2j.5b.36.0.4.5.26.9.7.5c.p.1.4.1.4.0.0.4h
M|Katherine M. Clark|D|H-MA-5|ao|9m|f2|7.94o.sz.2wp.be.0.0.5.5.f.8.c.1f9.k.d.1.0.2.c.0.4i
M|Jay Obernolte|R|H-CA-23|o7|bx|f1|3m.2h3.fy.0.5h.b4.j.1.1.53.d.3.41.l.0.0.3.4.g.0.4j
M|Richard E. Neal|D|H-MA-1|dq|94|f1|y.623.nj.uw.6q.1p.0.5.4.y.8.e.ki.j.0.0.2.2.0.0.4k
M|Max L. Miller|R|H-OH-7|gq|fm|ez|3g.2d1.8t.ex.51.n1.7zj.1.0.2p.a.0.f6.7.1.0.2.2.f.1.4l
M|Robin L. Kelly|D|H-IL-2|26|3w|ey|6v.1dm.a0.0.3o.zk.0.6.5.2z.a.0.c6.z.0.0.1.3.c.0.4m
M|Jennifer A. Kiggans|R|H-VA-2|f2|eh|ey|3o.2d7.g3.3i.4f.1qz.8rq.0.0.3l.1.j.6w.t.0.0.3.1.3.0.4n
M|Guy Reschenthaler|R|H-PA-14|oa|7q|ex|1n.48k.i2.31.5e.9r.0.2.1.15.k.5.19.m.0.0.1.1.1j.0.4o
M|Tammy Duckworth|D|S-IL|5i|71|ew|73.127.49.fj.20.1e.0.8.3.8y.q.j.32.0.0.0.4.1.0.0.4p
M|Yvette D. Clarke|D|H-NY-9|ef|gl|eu|6j.1gv.9a.0.3s.82.0.5.3.3y.f.6.dk.h.0.0.1.4.6.0.4q
M|Katie Boyd Britt|R|S-AL|n6|bg|er|w.7f1.9x.2.ay.0.0.2.0.3x.h.9.g4.0.a.k.5.0.b.0.4r
M|Andy Harris|R|H-MD-1|f6|fs|eq|90.z5.5s.0.25.f.1o.4.6.cp.f.3.8a.y.2.0.1.0.9.0.4s
M|Ryan K. Zinke|R|H-MT-1|no|8t|ep|59.22b.3i.23.4d.4f.38a.3.4.1h.j.5.5h.8.0.0.2.2.0.0.4t
M|Jimmy Gomez|D|H-CA-34|8q|4z|el|6e.1my.5d.0.3n.20n.nn.3.6.2d.a.7.8s.8.1.0.2.5.9.0.4u
M|Jon Husted|R|S-OH|eh|eg|ej|1c.4jw.ok.qt.96.1gaq.2s2w.0.0.3y.2.1.cn.0.0.0.5.0.4.0.4v
M|Nancy Mace|R|H-SC-1|75|cw|ej|ba.km.2x.22.1p.rh.2re.6.4.5a.j.d.42.4.0.0.3.3.h.1.4w
M|Jack Bergman|R|H-MI-1|qn|eo|ed|3h.21k.93.ps.3e.6h.a3.2.1.2f.h.6.54.4.0.0.3.4.0.0.4x
M|James Lankford|R|S-OK|mj|9m|ec|5m.1x2.5z.2.3l.0.0.7.7.7e.e.a.76.0.0.0.4.0.0.0.4y
M|Chrissy Houlahan|D|H-PA-6|2l|6q|ec|7b.1a1.8w.b.3n.64.0.1.5.2l.b.d.7t.s.1.0.2.2.s.2.4z
M|Vern Buchanan|R|H-FL-16|hn|f7|eb|6a.1kl.8w.9.2v.0.0.9.6.6y.e.6.8u.8.0.0.2.1.v.0.50
M|Nicole Malliotakis|R|H-NY-11|au|5d|eb|5r.1oc.b9.1n.3p.0.0.3.5.4n.d.5.3m.n.b.0.2.5.k.0.51
M|Frank D. Lucas|R|H-OK-3|h4|i9|eb|7v.14j.9t.0.2f.45.0.5.8.68.a.3.5p.r.0.0.2.3.0.0.52
M|Amy Klobuchar|D|S-MN|dt|7r|e8|a5.tc.4f.5.1n.1h.0.f.c.f9.8.a.2v.0.0.0.6.0.8.2.53
M|Angela D. Alsobrooks|D|S-MD|8p|9z|e7|e.7sn.9a.2k4.ft.2p9.3z7.1.0.1a.5.3.13p.0.0.0.4.1.0.1.54
M|Donald G. Davis|D|H-NC-1|7w|d4|e7|4u.1yp.g2.0.6g.773.6sv.0.1.28.i.0.3y.a.0.0.2.1.0.0.55
M|John Kennedy|R|S-LA|mk|aj|e6|62.1vj.2o.0.3d.0.0.a.6.bh.a.6.5v.0.1.0.4.0.5.0.56
M|Adam Smith|D|H-WA-9|9n|6g|e5|4b.2ck.ba.0.47.1.0.8.4.13.q.0.bc.7.e.2.1.4.m.0.57
M|Jon Ossoff|D|S-GA|5g|gq|e5|ac.od.69.1t.2r.396.3gm.7.4.3s.f.a.z.0.0.0.3.0.5.0.58
M|Alex Padilla|D|S-CA|3x|8p|e4|3r.2p6.3s.36.4m.0.0.4.6.9c.8.9.8w.0.0.0.7.2.0.0.59
M|Ashley Moody|R|S-FL|m9|eb|e2|1g.4ol.iq.hm.80.ph.6af.0.0.2e.4.2.xt.0.3.5.6.0.0.0.5a
M|Ronny Jackson|R|H-TX-13|n3|eg|e1|3i.21k.38.vj.2t.2.0.3.3.1t.q.0.5c.c.7.0.4.1.p.0.5b
M|Kevin Cramer|R|S-ND|ny|6d|e1|5x.1k4.ci.2i.3x.1.0.4.3.50.e.d.64.0.0.0.4.0.0.3.5c
M|Darren Soto|D|H-FL-9|3d|bd|e0|65.1h1.g0.1.3s.g8.je.3.6.1l.c.7.9a.e.0.0.2.4.0.0.5d
M|Lloyd Smucker|R|H-PA-11|7q|fd|e0|54.1ww.ch.0.30.0.0.5.3.70.6.8.26.n.1.0.3.3.i.0.5e
M|Richard J. Durbin|D|S-IL|72|92|dz|8z.ps.1q.di.1b.0.0.g.c.fy.n.g.5z.0.0.0.3.0.2.0.5f
M|Tim Walberg|R|H-MI-5|fl|46|dz|70.1bo.ah.0.2w.2.0.5.5.8l.c.1.4q.s.1.1.2.3.s.0.5g
M|Rick Larsen|D|H-WA-2|dd|6n|dz|3t.2dq.ib.0.5a.1.0.5.1.1m.b.4.9p.w.13.14.1.3.n.0.5h
M|Mike Kelly|R|H-PA-16|ea|6g|dz|5h.1uy.a6.0.3v.0.0.3.4.9y.d.0.55.7.8.5.1.2.1h.0.5i
M|Catherine Cortez Masto|D|S-NV|b8|b4|dx|33.322.3m.4h.2y.r.0.3.2.a9.6.5.6k.0.1.0.4.2.8.0.5j
M|Joe Neguse|D|H-CO-2|6p|el|dv|4w.241.94.0.46.0.0.3.5.7u.c.4.6w.d.0.0.3.4.0.0.5k
M|Lori Trahan|D|H-MA-3|4g|dy|dv|39.2vw.8d.0.5h.0.0.4.2.3s.d.5.32.d.0.0.1.5.1b.0.5l
M|Marcy Kaptur|D|H-OH-9|6t|fg|du|6i.1fr.an.0.3v.31m.3z2.6.7.i.c.3.6s.3.1.1.2.2.4.0.5m
M|Donald S. Beyer, Jr.|D|H-VA-8|5h|az|ds|5b.20t.6s.0.3s.0.0.2.5.4h.l.7.f6.i.1.0.2.5.2.0.5n
M|Mike Levin|D|H-CA-49|7r|gm|dr|6f.1mh.4r.f.3h.5r.3y.0.8.2k.c.3.6o.7.0.0.1.6.0.2.5o
M|Brad Finstad|R|H-MN-1|k4|fj|dr|8k.vg.bm.w.24.97.420.1.3.3y.i.3.13.c.0.0.3.2.0.0.5p
M|Randy Feenstra|R|H-IA-4|lw|dt|dq|4a.27n.gb.0.42.25.0.2.2.62.8.6.9e.e.0.0.2.1.e.0.5q
M|Debbie Dingell|D|H-MI-6|8v|7j|dq|7f.17l.9d.1i.2h.3.0.5.9.5z.8.5.2s.6.x.8.2.4.0.0.5r
M|Richard Blumenthal|D|S-CT|ar|d1|do|7t.1cc.2d.0.22.0.0.d.a.bi.a.e.7y.0.0.0.5.0.5.0.5s
M|Dina Titus|D|H-NV-1|d2|ci|dn|b9.l5.4t.0.2z.ih.1.6.8.4t.p.e.1x.4.0.0.2.3.s.0.5t
M|Neal P. Dunn|R|H-FL-2|gu|at|dm|53.1zq.9v.k.4t.0.0.3.5.6h.8.3.41.g.3.2.2.2.2i.0.5u
M|Greg Stanton|D|H-AZ-4|7d|a9|dm|8m.11o.63.0.2w.ms.23.3.2.1r.e.a.3v.d.1z.3x.3.1.0.0.5v
M|Kat Cammack|R|H-FL-3|r5|m|dj|5s.1no.90.4k.3k.46.0.3.2.4b.b.3.19.i.0.0.2.2.1.0.5w
M|Dan Crenshaw|R|H-TX-2|ms|4y|dg|99.un.8o.m.2f.tl.bd.1.0.95.d.3.2p.i.4.3.2.2.e.0.5x
M|Daniel Meuser|R|H-PA-9|ls|ai|df|6s.1ey.95.0.2o.0.0.4.5.1w.a.5.4o.a.v.b.2.1.5.7.5y
M|Glenn Thompson|R|H-PA-15|l7|ck|df|51.1wc.fj.3.3s.43.2.1.2.fw.4.0.6e.1c.0.0.2.6.0.0.5z
M|Angus S. King, Jr.|I|S-ME|dz|66|df|76.1ak.a5.4.3a.g.0.4.5.33.h.d.9r.0.m.v.4.1.0.0.60
M|Josh Hawley|R|S-MO|np|4n|df|9r.pq.2g.7w.1m.v6.aj.4.3.94.b.5.3k.0.1.0.4.0.0.0.61
M|Jim Jordan|R|H-OH-4|mp|dy|de|1o.40u.az.ff.4w.4.4.2.6.2.b.3.6k.20.0.0.2.0.0.1.62
M|Seth Moulton|D|H-MA-6|9g|59|dc|9y.w9.2w.1.1u.1rb.1pq.1.7.17.m.9.1e.b.4.8.3.5.1j.1.63
M|Chris Van Hollen|D|S-MD|8j|ds|dc|96.v6.19.81.1t.0.0.8.b.8t.n.q.2s.0.0.0.4.1.2.0.64
M|Greg Landsman|D|H-OH-1|93|bo|dc|61.1qp.7l.0.6j.1fk.vf.0.2.2e.6.3.70.j.t.j.1.1.s.0.65
M|Michael T. McCaul|R|H-TX-10|bu|6f|db|a7.sm.50.0.2c.t.0.3.9.4u.11.k.94.r.0.0.2.2.2o.0.66
M|Donald Norcross|D|H-NJ-1|c9|6u|da|91.ws.7r.9.1v.2.0.8.9.3y.e.9.76.d.2.0.2.2.20.0.67
M|Raphael G. Warnock|D|S-GA|57|6o|d9|5v.1tb.o.63.2x.bq.0.2.5.37.a.a.pd.0.0.0.4.1.0.0.68
M|Troy Balderson|R|H-OH-12|l9|en|d8|3e.2nq.ea.0.4x.2.0.3.0.3q.b.1.36.v.0.0.1.4.a.0.69
M|Chuck Grassley|R|S-IA|6n|8w|d7|9b.109.1p.1t.1y.j.0.c.f.b6.9.a.4t.0.0.0.6.0.0.0.6a
M|W. Gregory Steube|R|H-FL-17|dx|27|d6|7d.1bi.6o.c.40.0.0.3.3.53.f.8.1u.s.0.0.2.3.0.1.6b
M|William R. Timmons IV|R|H-SC-4|f7|gs|d5|6o.1gd.84.f.2w.1ve.0.4.4.1l.8.4.3z.9.1.2.2.1.2.0.6c
M|Jared Moskowitz|D|H-FL-23|ff|ac|d3|97.yr.4l.13.37.1vm.adn.1.1.14.f.h.8q.c.1u.3q.3.1.j.0.6d
M|Rick W. Allen|R|H-GA-12|ej|78|d3|8y.yf.6m.0.1q.0.0.6.4.5j.b.2.2k.i.10.2n.2.3.0.0.6e
M|Mazie K. Hirono|D|S-HI|5e|9w|cz|6b.1ll.83.0.3n.2.0.7.5.3m.f.9.1t.0.0.0.5.1.0.0.6f
M|Trent Kelly|R|H-MS-1|oc|9h|cw|4x.263.6t.0.2z.0.0.4.8.2d.m.0.3u.2.0.0.3.1.3.0.6g
M|Tommy Tuberville|R|S-AL|lg|4c|cw|82.19s.2c.m.2e.3i.5.4.1.3k.b.c.2x.0.21.df.5.0.0.0.6h
M|Mark E. Amodei|R|H-NV-2|dv|54|cv|8e.153.4t.3.1s.0.g.3.7.c2.a.3.1w.9.1.0.2.6.0.0.6i
M|Rand Paul|R|S-KY|d4|5a|cv|9x.v7.2i.1j.1j.2n.0.9.c.47.f.c.32.0.0.0.4.0.0.0.6j
M|Gabe Amo|D|H-RI-1|4q|9b|cu|2i.3k6.87.0.8z.22.0.2.3.10.h.5.b1.6.0.0.3.2.0.0.6k
M|Brad Sherman|D|H-CA-32|4j|ea|cu|a2.ru.67.0.17.r2.0.c.4.1e.p.a.2n.0.0.0.2.5.0.0.6l
M|John H. Rutherford|R|H-FL-5|pg|79|cu|5f.1ye.73.0.35.2j.0.3.2.1r.d.2.5f.h.2.0.1.2.i.0.6m
M|John R. Moolenaar|R|H-MI-2|k2|it|ct|55.1x2.bf.4.3b.2.0.2.3.4o.9.7.59.n.0.0.2.2.6.0.6n
M|Ted Lieu|D|H-CA-36|k|a0|cs|7o.12r.6w.6u.2h.2y.0.3.3.2c.l.b.9b.o.0.0.2.4.7.0.6o
M|Austin Scott|R|H-GA-8|kw|f5|cs|8d.14w.59.0.1u.47.2.4.9.n.k.0.34.l.7.2.4.3.8.0.6p
M|Charles E. Schumer|D|S-NY|b1|8h|cs|8f.16k.37.0.1i.0.0.x.n.48.d.d.5q.0.0.0.2.0.f.0.6q
M|Ben Cline|R|H-VA-6|pe|ga|cr|6g.1io.87.0.32.4g.0.0.4.2s.e.2.19.j.0.0.4.2.v.1.6r
M|Nick LaLota|R|H-NY-1|r6|s|cr|5c.1s4.82.69.3h.3k.146.0.2.2u.9.5.37.a.0.0.2.4.s.0.6s
M|Cory A. Booker|D|S-NJ|6a|cf|cq|cg.9m.51.2z.1m.3.0.a.8.9v.w.k.p.0.5.4.4.3.2.0.6t
M|James E. Clyburn|D|H-SC-6|8b|6i|cp|4d.29c.du.0.3p.2.0.6.8.n.e.5.9d.6.2.0.1.2.0.0.6u
M|Pete Stauber|R|H-MN-8|nj|ba|cp|6n.1bj.by.1l.3c.d.go.0.3.4f.7.3.29.n.1.1.3.5.9.0.6v
M|Stephanie I. Bice|R|H-OK-5|p4|5l|cp|47.2cy.b5.u.4f.2l.0.3.0.27.7.3.34.i.0.0.2.1.h.1.6w
M|Jim Costa|D|H-CA-21|80|6p|cp|8l.xy.9s.4.2b.0.0.7.7.2d.p.6.2a.h.1.0.2.4.g.0.6x
M|Eric Sorensen|D|H-IL-17|5f|5v|cl|5t.1t3.7j.5.4s.qc.2f.0.3.1z.9.3.2w.7.1.0.2.0.0.1.6y
M|Kim Schrier|D|H-WA-8|n|n|ci|63.1nx.a0.0.5p.8r.0.1.4.2x.9.0.3k.n.0.0.1.2.4.0.6z
M|Mike Flood|R|H-NE-1|cm|gz|ch|74.19m.bd.w.2z.5e.243.1.1.38.7.1.2n.m.1.0.1.2.0.0.70
M|Vince Fong|R|H-CA-20|ih|79|cg|52.20h.b7.0.4y.fm.0.2.1.1q.2.2.56.g.c.0.3.1.7.0.71
M|Harriet M. Hageman|R|H-WY-0|gh|3s|cf|7w.13y.6n.3q.2f.uk.0.0.3.3e.5.4.2n.f.1e.0.3.3.b.0.72
M|Pete Sessions|R|H-TX-17|m4|93|ce|ao.or.59.0.1x.1.0.b.6.1v.l.6.3y.f.14.1b.2.3.0.0.73
M|Gabe Evans|R|H-CO-8|54|ek|cd|6t.17w.b9.4o.3k.2wu.h4w.0.1.41.4.0.2c.d.0.0.2.1.0.0.74
M|Scott Fitzgerald|R|H-WI-5|r6|n|cd|46.2hk.8o.0.3u.5a.0.1.2.3l.5.3.3c.e.0.0.2.2.1j.0.75
M|James Comer|R|H-KY-1|bs|5c|c9|5i.1tv.ah.6.39.0.0.2.4.3g.7.2.4g.1f.4.6.2.3.0.0.76
M|Nikki Budzinski|D|H-IL-13|5l|58|c8|3y.2hx.bz.g.6k.jz.0.0.2.1o.8.3.55.i.0.0.2.1.0.0.77
M|Patrick Ryan|D|H-NY-18|4d|df|c7|77.1ev.45.1f.3q.1uu.1z.0.1.1a.g.n.bv.6.a.0.2.1.0.0.78
M|Vicente Gonzalez|D|H-TX-34|7m|bs|c6|7i.142.dc.c.2y.2hs.666.0.7.p.9.b.6e.8.0.0.1.3.1.0.79
M|Adriano Espaillat|D|H-NY-13|6l|89|c5|8r.12s.3t.0.2i.3us.t0.1.4.2e.a.8.eo.4.0.0.1.4.0.0.7a
M|John Hoeven|R|S-ND|pa|84|c5|9h.y8.2t.18.1o.0.0.9.6.78.d.8.3f.0.0.0.4.0.5.0.7b
M|Russell Fry|R|H-SC-7|oo|cr|c4|57.20e.7e.6.4h.vy.0.0.3.2h.7.3.6e.7.0.0.2.2.c.0.7c
M|Ralph Norman|R|H-SC-5|ab|3t|c1|e1.6i.w.0.i.ed.3w8.5.4.1m.g.3.k.j.e.0.3.3.0.0.7d
M|Celeste Maloy|R|H-UT-2|nb|4a|c0|3d.2sn.9u.2.3s.13q.93.0.1.1q.6.2.14.a.0.0.2.1.4.0.7e
M|Byron Donalds|R|H-FL-19|m7|8m|bz|94.yp.3v.23.22.0.e.3.5.4w.8.4.d9.b.f.9.2.4.0.0.7f
M|Brendan F. Boyle|D|H-PA-2|ax|bt|bz|68.1m7.a3.0.3v.4c.0.0.5.1m.e.a.6c.d.1.0.2.5.2b.0.7g
M|Raul Ruiz|D|H-CA-25|8g|f9|bz|7q.16w.9h.0.2w.0.0.6.4.6f.7.4.5m.e.0.0.1.2.9.0.7h
M|Nathaniel Moran|R|H-TX-1|o8|m|by|7c.1as.7k.p.3g.5n.0.0.1.3l.d.a.49.f.0.0.3.1.19.1.7i
M|Erin Houchin|R|H-IN-9|k5|54|bu|4i.23g.bc.62.43.0.1d.2.1.3k.6.1.1m.i.0.0.3.2.n.0.7j
M|Dusty Johnson|R|H-SD-0|n6|gg|bs|7u.13h.ak.m.2y.3h.0.1.2.6k.a.0.1t.m.0.0.3.4.1.0.7k
M|Marie Gluesenkamp Perez|D|H-WA-3|80|fn|bs|6d.1go.6l.5a.52.1o4.9oy.0.0.3j.3.3.o.8.0.0.1.3.0.0.7l
M|Diana Harshbarger|R|H-TN-1|22|fo|bq|5l.1sl.af.5.3f.e.0.2.2.5i.7.2.p.a.0.0.1.3.e.0.7m
M|Emanuel Cleaver|D|H-MO-5|53|b7|bp|9k.ve.6a.0.1n.6j.0.7.6.1s.7.6.5k.d.1.0.1.3.0.0.7n
M|Troy A. Carter|D|H-LA-2|8d|96|bp|49.2az.br.1o.4i.0.0.0.4.1u.c.0.7d.q.0.0.2.4.c.1.7o
M|Marilyn Strickland|D|H-WA-10|4v|59|bp|5y.1rc.7h.0.4a.aw.0.0.4.15.8.d.5x.j.0.0.2.3.1g.0.7p
M|Rudy Yakym III|R|H-IN-2|91|hq|bn|4l.203.d2.6o.4r.5c.0.1.0.2t.8.3.u.b.0.0.1.1.a.0.7q
M|James R. Baird|R|H-IN-4|r8|4x|bm|d7.a5.2z.0.u.es.5k.2.4.3x.p.5.14.t.0.0.3.2.3.0.7r
M|Steny H. Hoyer|D|H-MD-5|7h|cr|bk|6m.1e6.64.4w.1w.2.0.e.a.b.b.2.64.j.1.0.1.0.y.0.7s
M|Robert C. "Bobby" Scott|D|H-VA-3|ee|55|bh|bg.m7.2s.0.1w.0.0.4.8.4t.a.0.3z.r.4.0.2.4.0.1.7y
M|Joyce Beatty|D|H-OH-3|lu|b1|be|7e.184.af.0.2k.1.0.5.6.x.c.5.9o.6.5.0.1.3.6.1.82
M|Bill Foster|D|H-IL-11|43|2r|b4|a9.o6.8s.0.1t.2v.s.8.a.1p.9.1.0.9.0.0.2.2.0.1.8f
M|Mark Alford|R|H-MO-4|o2|8x|b3|6h.1jz.6k.0.3k.0.0.2.1.1u.c.2.2s.f.3.1.2.2.l.1.8j
M|Steve Cohen|D|H-TN-9|j7|3h|az|c7.ez.3v.0.1i.0.0.5.4.3c.e.a.55.8.k.2.2.4.1s.1.8l
M|Mike Collins|R|H-GA-10|k2|g1|a2|c3.df.4q.18.14.1tz.b4o.0.1.4p.7.1.u.6.0.0.3.2.0.1.9f
M|Lloyd Doggett|D|H-TX-37|f8|dl|9y|db.bm.x.0.q.0.0.6.8.3n.b.5.1m.3.7.23.3.2.m.1.9m
M|Cliff Bentz|R|H-OR-2|kf|41|9p|6p.1hf.7f.0.3v.0.0.0.3.28.5.2.23.8.c.1.2.3.0.1.9v
M|Monica De La Cruz|R|H-TX-15|az|fh|9o|a6.ni.84.25.1a.1ev.8ro.2.2.19.3.1.0.3.0.0.2.2.0.1.9w
M|Janelle S. Bynum|D|H-OR-5|b5|g6|9j|6w.1fx.75.1.5h.3tr.1uw.0.1.j.4.1.w.5.0.0.1.1.0.1.9z
M|Roger Williams|R|H-TX-25|ig|4e|9f|bt.hd.47.d.1c.d.0.2.1.76.5.0.1j.9.c.4.2.1.0.1.a3
M|Carlos A. Gimenez|R|H-FL-28|hq|38|9c|b3.mi.3i.1i.18.0.0.3.4.16.j.9.30.c.2.0.3.4.1c.1.a5
M|Glenn Ivey|D|H-MD-4|n7|44|8w|7j.1f6.2b.0.2s.5.0.1.0.10.8.4.62.d.5.0.2.2.5.1.ag
M|Adam Gray|D|H-CA-13|51|cq|8p|8c.113.8m.j.3n.1by.352.0.0.u.3.1.p.3.1.0.2.0.6.1.am
M|Abraham J. Hamadeh|R|H-AZ-8|qj|fl|8m|dz.5b.22.9.p.fy.gs.2.3.1p.2.c.0.6.0.0.2.0.0.3.aq
M|Andy Biggs|R|H-AZ-5|nw|fl|8m|em.2i.3.0.b.0.0.2.4.6k.a.1.f.j.2.0.2.3.0.1.as
M|Sanford D. Bishop, Jr.|D|H-GA-2|m|26|7x|8v.w4.9n.1.1g.5.0.2.3.c.a.1.bz.a.0.0.1.4.0.1.bg
M|Jimmy Patronis|R|H-FL-1|ko|4a|7f|al.ry.2d.d.1x.1y8.1a.0.0.d.4.0.97.3.b.0.2.0.4.1.by
M|Russ Fulcher|R|H-ID-1|6t|19|7e|cc.ew.3f.0.17.0.0.2.5.29.a.3.5.4.0.0.2.2.b.1.c0
`;
const RSB = `
M|Danny K. Davis|D|H-IL-7|2a|3p|6x|dr.7f.1i.0.l.1d.0.4.1.1z.a.0.0.2.0.0.1.4.0.1.cd
M|Nikema Williams|D|H-GA-5|o|55|6a|c9.es.3x.0.15.6.0.1.3.21.6.0.1t.8.0.0.1.3.0.1.cy
M|Marlin A. Stutzman|R|H-IN-3|oz|h7|5x|ct.ew.a.h.1q.ax.0.1.1.g.4.1.5.f.0.0.2.0.0.1.da
M|David J. Taylor|R|H-OH-2|el|4c|5u|dj.8b.2q.0.y.1l.2.0.1.1s.7.2.10.5.8.1o.2.0.0.1.df
M|Mike Kennedy|R|H-UT-3|oc|4h|5l|8q.137.3x.3.2i.6.0.0.1.13.4.0.f.1.0.0.3.1.8.1.do
M|Frederica S. Wilson|D|H-FL-24|2g|do|59|e3.5s.18.0.j.0.0.2.2.1q.6.0.32.5.0.0.2.5.0.2.dz
M|Gilbert Ray Cisneros, Jr.|D|H-CA-31|de|dx|4g|cl.fw.13.0.1c.7.1.0.0.7.0.d.k.4.6r.5e.2.4.0.1.ec
M|Alan Armstrong|R|S-OK|o5|5b|33|ep.1m.0.0.8.0.0.0.0.k.0.0.0.0.2z.36.2.0.0.2.eo
M|Kelly Morrison|D|H-MN-3|na|4k|2s|ei.20.1m.0.7.1.0.0.0.v.3.1.0.2.d.q.2.1.7.1.eq
L|John Breaux|D|Crossroads Strategies, LLC|ci|aq|mc|1.nd.l5.nx.4.35u.1f.3s.t.7u.h.1ec.z.0.0.2.k.0.5.0.0.2
L|John Gonzalez|D|Tiber Creek Group|ba|7x|m6|2.ob.5k.ow.0.55f.1c.2s.5.1ji.1t.1wy.8s.1.1.0.6h.1.2.0.1
L|Jose Borjon|D|Akin Gump Strauss Hauer & Feld|dp|da|lw|3.pj.7.q6.0.8cg.2v.2u.11.171.1r.6z.22.1.3.0.1w.1
L|Jeffrey Miller|R|Miller Strategies, LLC|k0|br|lt|4.ox.1d.p1.0.110i.6h.1f.1v.4ir.2v.7np.1wl.0.0.2.50.1
L|Nadeam Elshami|D|Brownstein Hyatt Farber Schrec|af|8y|ln|5.pl.6.q0.0.693.3y.31.1h.fu.17.js.5e.0.4.0.1j.1
L|Landon Stropko|R|Invariant LLC|l3|ar|ll|6.p1.13.px.0.4lo.1b.24.m.qq.15.ko.3w.3.d.0.0.0.0.4
L|Israel Klein|D|Klein/johnson Group|9p|7q|ld|7.p0.16.pu.0.2yo.1g.29.x.1f5.25.nh.6m.2.0.0.29.1
L|Heather McHugh|D|Resolution Public Affairs, LLC|9g|96|lc|8.p8.k.pq.0.3li.13.1t.5.la.o.j6.4g.3.2.0.1u
L|Ryan Berger|R|Navigators Global LLC (Formerl|ht|d3|l7|9.oa.5y.p8.0.3eb.18.2q.t.7l.j.5z.17.4.0.0.0.2
L|Andrew Usyk|D|Brownstein Hyatt Farber Schrec|aa|83|l2|a.pg.c.pu.0.4xq.33.2y.1b.h0.14.e9.54.3.0.0.5.1.0.0.0.4
L|Virgil Miller|D|Akin Gump Strauss Hauer & Feld|7r|aw|l2|b.o6.7j.og.0.57e.28.29.h.9n.w.4a.2m.3.0.0.a.0.0.0.1.0.0.0.1
L|Karissa Willhite|D|OGR|ak|8c|l0|c.o5.86.or.0.3yu.1q.4x.p.15w.1r.cy.3m.2.0.0.a.0.1
L|Anne Macmillan|D|Invariant LLC|av|ct|kx|d.p6.r.q3.0.5mr.17.1g.i.xx.22.2pp.3n.2.1.0.a.0.0.1.0.3
L|Michael Robinson|R|Mehlman Consulting, Inc.|gs|6f|kw|e.nj.hx.oc.0.3b8.4c.dh.14.o4.n.3c.17.0.3.0.0.0.5
L|Kevin Casey|D|S-3 Group|ch|86|kv|f.ox.1e.pt.0.382.1e.u.4.u7.16.co.3h.5.0.0.1o
L|Marne Marotta|R|Arnold & Porter Kaye Scholer L|jh|9f|kv|g.p1.14.pa.0.1z0.1b.12.1f.1j5.4c.bi.42.3.0.0.z.1
L|Lauren Aronson|D|Mehlman Consulting, Inc.|9j|77|kv|h.nw.ca.oi.0.39l.3y.d8.13.q3.1j.c6.24.0.2.0.5.0.0.3.0.4.0.0.1
L|Sandra Alcala|D|Avoq, LLC|a1|cm|kt|i.of.43.p6.0.2aq.s.14.c.f5.q.ds.2i.3.o.0.23
L|Zachary Pfister|D|Brownstein Hyatt Farber Schrec|bl|b7|ks|j.ov.1p.of.0.5z3.3b.2i.1c.7w.z.am.3t.3.0.0.2.1
L|ANN Jablon|D|Capitol Counsel LLC|bd|99|ks|k.p0.18.py.0.5g2.24.3p.g.mi.18.8m.31.1.0.0.a.2
L|Stuart Chapman|D|Thorn RUN Partners|ad|9c|ks|l.oe.4j.oo.0.4dy.x.1g.7.r0.16.bg.4e.4.0.0.c
L|Todd Wooten|M|Holland & Knight LLP|es|7s|kr|m.ow.1g.op.0.43h.1q.20.q.p3.27.78.1i.2.0.0.0.1.1.0.0.1
L|Edward Ayoob|D|Barnes & Thornburg, LLP|bj|by|kp|n.og.3t.og.0.2pj.r.1j.m.1s9.4m.en.4y.1.0.0.2d.2
L|Matt Bravo|R|S-3 Group|j7|9o|kp|o.p2.12.px.0.5v2.28.u.4.uq.o.fp.4x.3.0.0.0.2
L|Pamela Smith|D|Tarplin, Downs & Young, LLC|aa|af|ko|p.oi.3e.or.0.4g4.1y.2i.c.1dq.12.mq.9f.1.0.0.37.0.1
L|Rachel Miller|D|Forbes-Tate|bs|95|ko|q.nt.d7.od.0.3um.1b.2e.i.f4.n.6y.3f.2.0.0.a.1
L|Thomas Andrews|R|Squire Patton Boggs|gf|bj|kn|r.oe.4i.oi.0.6nu.2f.x.11.d0.o.98.4y.2.0.1.0.2.2
L|Jerome Murray|D|OGR|87|7g|kl|s.oh.3i.pm.0.32s.1b.4d.m.ke.1e.4s.x.3.1.0.5
L|Sudafi Henry|D|Thegroup DC, LLC|8f|ar|kl|t.p8.q.q4.0.4ir.r.y.7.1cx.1c.na.at.2.0.0.f.1.0.0.0.4
L|Joel Bailey|D|BGR Government Affairs|db|b2|kl|u.ob.5i.ok.0.5j3.25.4.r.d5.11.8w.2m.2.4.0.u.2.0.0.0.1
L|Paul Edattel|R|Todd Strategy Group|fp|cp|kk|v.od.4l.oz.0.6ei.2m.2b.8.31m.2l.xa.b9.1.0.0.1j.0.0.1
L|Dean Aguillen|D|OGR|9d|7i|kj|w.oj.3a.po.0.379.1a.3w.l.p0.19.3p.15.1.1.0.m
L|Christopher McCannell|M|Grayrobinson PA|ag|a2|ki|x.oq.2b.p0.0.1qs.11.19.o.w4.2l.xh.1v.5.0.0.a.0.1.0.0.0.0.0.0.8
L|Lindley Sherer|R|Invariant LLC|kb|5o|ki|y.o2.9b.oo.0.1dz.h.2l.8.3cd.1i.ls.2i.3.0.0.2s
L|Christopher Davis|D|Capitol Hill Consulting Group|cc|b4|ki|z.n0.r0.n9.0.2nk.r.i.b.4g.8.6e.o.2.1.0.f.0.3.0.0.0.0.1.0.23
L|William Moschella|R|Brownstein Hyatt Farber Schrec|ie|be|ki|10.om.2t.oq.0.517.22.1x.y.ji.1y.ku.56.1.0.0.a.2
L|Paul Bock|D|Thorn RUN Partners|a3|ch|kg|11.o7.77.og.0.2yx.t.q.6.yk.1b.br.3r.1.0.0.1e.0.4
L|Mark Pryor|D|Brownstein Hyatt Farber Schrec|c5|7y|kf|12.na.m8.mz.0.1i9.1j.14.x.7d.r.rd.3d.0.0.2.a.2.0.0.0.1
L|Kyle Nevins|R|Harbinger Strategies, LLC|lp|8w|kf|13.o9.69.ow.0.6go.23.3x.e.154.1g.c7.6h.2.0.0.0.1
L|John O'Neill|R|Colton Street Group|ks|6b|ke|14.nr.dz.oo.0.821.1m.1e.a.jm.q.3j.15.1.1.0.0.1.2
L|Elizabeth Murray|D|Tarplin, Downs & Young, LLC|8e|cg|kd|15.ot.1t.ps.0.4qp.20.2k.b.dm.p.32.r.1.7
L|Emily Katz|D|VAN Scoyoc Associates|d8|7e|kc|16.os.23.p2.0.1ww.q.1c.8.rk.o.1ma.3p.3.0.0.p
L|James Ryan|D|Avoq, LLC|cs|7o|kc|17.ne.ke.o2.0.3od.t.19.c.9o.e.q5.q.1.1.0.x.0.1.0.0.0.0.1
L|Jeffrey Shapiro|R|Tiber Creek Group|ic|9w|kc|18.ok.32.pl.0.3ee.w.4w.s.j4.r.3w.24.2.0.0.0.0.1.0.2.0.0.0.0.2c
L|John Reising|R|Brownstein Hyatt Farber Schrec|hu|cu|kb|19.ox.1f.pj.0.3cp.3c.1k.1h.94.13.3v.1f.3.0.0.0.1.0.0.0.2
L|ED Pagano|D|Akin Gump Strauss Hauer & Feld|dx|8u|kb|1a.p8.o.ov.0.6hd.2h.33.r.10m.1d.lw.7e.0.2.0.1o
L|Brandt Anderson|R|Brownstein Hyatt Farber Schrec|e3|bl|kb|1b.pc.i.ps.0.411.2c.10.17.bu.1a.7z.3g.4.0.0.0.1.0.0.0.3
L|Zachary Mallove|D|Mehlman Consulting, Inc.|9r|6u|ka|1c.nu.cu.p2.0.3fb.4d.dt.14.4s.l.44.b.1.0.0.2k
L|Travis Johnson|R|1607 Strategies, LLC|jf|bs|ka|1d.ny.b6.oe.0.2jr.11.16.o.4bj.2f.1em.ik.3.0.0.k
L|Elizabeth Kelley|D|The Duberstein Group Inc.|9i|ak|ka|1e.nx.bm.oi.0.3jg.14.i.k.r0.v.gx.2h.3.0.0.2i
L|Jerr Rosenbaum|R|Penn Avenue Partners|gg|9j|ka|1f.ot.1x.pw.0.4s2.14.2b.w.t9.u.37.2o.4
L|Mary Stanton|D|Invariant LLC|9a|az|k9|1g.oa.62.ou.0.443.r.3d.p.3ct.2n.1dg.dh.0.2.0.aq
L|Nichole Distefano|D|Mehlman Consulting, Inc.|92|70|k9|1h.no.fh.oe.0.3rz.4k.du.15.cr.14.7s.10.1.0.0.1y
L|Steve Stombres|R|Harbinger Strategies, LLC|j2|ay|k8|1i.o8.6u.ov.0.6rx.24.3z.e.yq.1e.cd.3l.1.0.0.1e
L|John Weber|R|Monument Advocacy|m3|f6|k8|1j.lo.1if.op.0.2fv.t.1v.o.4q.f.0.0.3.0.0.0.0.7
L|Drew Griffin|R|Invariant LLC|iw|e9|k7|1k.ov.1o.pr.0.3mt.1e.3c.m.ms.15.d2.2g.3
L|Thomas Davis|R|Holland & Knight LLP|me|cw|k7|1l.o0.a8.o2.0.2xk.r.g.g.ba.q.64.2z.0.1.2.0.1.3
L|Logan Hollers|D|Invariant LLC|6j|bb|k6|1m.oi.3g.pp.0.3nn.10.1o.e.b4.19.6q.l.2.0.0.a.0.0.0.0.6
L|Chris Miller|R|Crossroads Strategies, LLC|l7|9s|k5|1n.n4.p8.oc.0.47x.2e.6s.13.c6.n.24.7.3.1
L|Jonathan Hiler|R|Miller Strategies, LLC|g3|bv|k4|1o.p2.z.py.0.901.1k.u.14.im.y.iz.4l.3.0.0.0.1.0.0.0.0.0.0.1
L|William Miller|R|American Gaming Association|fr|dg|k4|1p.mv.tm.mc.0.1ky.1.s.a.3x.6.dk.3k.0.4.0.1k.0.5.0.0.0.0.0.1.z
L|Mike McKay|D|Empire Consulting Group|ae|aw|k4|1q.p8.m.q4.0.4on.14.r.n.29s.1v.3ec.ah.1.0.0.uk.1.0.0.0.0.0.0.0.2v
L|SAM Geduldig|R|Cgcn Group, LLC|jd|bi|k4|1r.o4.89.oo.0.3c5.1t.95.a.2ij.1p.zq.5w.1.0.0.a.1
L|Ryan Mulvenon|D|Cassidy & Associates, Inc.|7y|9l|k3|1s.ot.1v.pr.0.4e7.10.1s.l.md.n.5w.2r.2.0.0.0.0.0.1
L|Andrea Larue|D|NVG, LLC|81|9y|k3|1t.nq.em.o6.0.2df.j.1w.6.sw.20.h4.3n.1.1.0.2a
L|Tucker Shumack|R|OGR|gl|7n|k3|1u.o1.9m.on.0.3th.1h.5f.o.xo.17.gc.2r.2.1
L|JAN Beukelman|D|Tiber Creek Group|ah|6v|k3|1v.m8.172.mv.0.1qk.p.3a.e.4g.g.4q.d.3.0.0.z.0.0.0.0.9
L|Naveen Parmar|D|Mehlman Consulting, Inc.|ct|a8|k3|1w.n6.oe.of.0.24p.40.c7.10.3a.j.16.f.3.0.0.5.0.0.0.0.2
L|Langston Emerson|D|Mindset Advocacy, LLC|6u|9l|k3|1x.nz.ao.oh.0.2uy.1b.m.e.1o8.1h.p7.4h.2.0.0.7w.0.0.0.0.1
L|Kevin O'Neill|R|Arnold & Porter Kaye Scholer L|cp|d1|k2|1y.of.46.ok.0.2v9.14.3i.x.2tf.3d.jt.47.0.0.0.6r.1.2.0.1
L|BEN Miller|D|Kadesh & Associates, LLC|6f|dw|k2|1z.my.ry.oq.0.2gg.t.39.h.5z.g.o.2.2.0.0.i
L|Jane Lucas|R|Alston & Bird LLP|f6|cp|k2|20.pi.9.q0.0.5hk.1u.1c.n.ra.16.bx.3w.1.0.0.5.0.0.2
L|Marc Lampkin|R|Brownstein Hyatt Farber Schrec|gu|7a|k2|21.oq.2a.ov.0.634.2h.1x.1h.116.1i.s8.8a.0.0.0.2j.1.2.0.0.1.0.0.1
L|David Bridges|R|Capitol Counsel LLC|jv|93|k1|22.ow.1i.pq.0.351.16.20.a.12k.15.e4.6x.2.0.0.0.1
L|Zachary Rudisill|R|Akin Gump Strauss Hauer & Feld|ja|82|k1|23.op.2i.ov.0.aqg.20.1m.h.w5.17.ng.6d.3
L|David Olander|R|Capitol Counsel LLC|jg|9t|k0|24.nx.bk.oj.0.32s.16.2v.a.1ci.1f.55.5x.2.0.0.0.1
L|Michael Gaffin|D|The Smith-Free Group, LLC|b5|aa|k0|25.lo.1ia.mu.0.1x3.o.3w.b.3c.d.1d.2.5.m.0.i
L|Sarah (Beatty) Rogers|R|Navigators Global LLC (Formerl|fj|au|k0|26.m9.16m.o6.0.3me.14.2s.r.8m.o.5.2.3.1.0.0.1.0.0.1.0.0.1
L|John Christie|D|The Smith-Free Group, LLC|1j|ct|k0|27.ni.ip.os.0.26j.t.58.a.5e.v.2x.8.2.0.0.a
L|Tyler Stephens|R|Fierce Government Relations|gi|8j|k0|28.oc.52.om.0.432.2s.8l.17.w5.t.ho.27.0.2.0.f.0.0.0.0.1
L|Scott Riplinger|R|Cgcn Group, LLC|hj|8e|jz|29.o0.9z.oj.0.40m.1v.9l.c.jl.w.id.9c.2
L|Corey Malmgren|D|Tiber Creek Group|bv|am|jz|2a.o2.9c.oq.0.7c6.19.3j.5.lz.y.9v.2i.1.0.0.p.0.0.0.0.1
L|Emily Kirlin|R|Tiber Creek Group|ki|an|jz|2b.nw.c4.p2.0.3c3.z.3e.e.5p.h.1y.u.3
L|Salim Alameddin|R|Crossroads Strategies, LLC|jc|cl|jz|2c.no.f6.p4.0.5tq.3c.89.16.3e.i.1x.8.2
L|Alanna Temme|R|LMH Strategic Solutions|gy|bh|jy|2d.o8.6n.og.0.4zx.1j.2y.5.gc.h.7l.1v.1.0.0.0.0.0.2
L|Jennifer Latourette|R|VAN Scoyoc Associates|km|7u|jy|2e.n9.mu.nj.0.21i.i.3m.f.9z.l.2v.1m.2.0.0.f.0.0.0.0.3
L|Elizabeth Stanley|D|Resolution Public Affairs, LLC|99|7z|jy|2f.ou.1s.pn.0.35u.z.1q.5.eb.1a.40.13.3.1
L|Kevin Yoder|R|Venture Government Strategies|gq|bw|jy|2g.mo.x2.pr.0.5jp.1b.3f.u.ae.1d.d.0.1.0.2.0.0.0.0.0.1
L|Manny Rossman|R|Harbinger Strategies, LLC|kj|7d|jy|2h.nc.lj.ow.0.6dw.23.3x.e.158.1i.2x.1.2.1
L|Milan Dalal|D|Tiger Hill Partners LLC|7j|c2|jy|2i.ow.1h.ps.0.4nd.s.3.1.gi.l.9y.41.2.0.0.s.1.1.0.0.1
L|Mark Rayder|R|Alston & Bird LLP|g5|eq|jy|2j.od.4m.ok.0.2ye.1a.3f.d.213.35.6q.3n.2.1
L|Sarah Egge|D|Splitoak Strategies LLC|bc|ao|jx|2k.nw.bu.ok.0.3jb.h.20.7.rl.1c.1ft.1e.1.0.0.p.0.0.1.0.1
L|TOM Tilton|D|Troutman Strategies|5m|7u|jx|2l.nn.g2.ny.0.2tu.1a.1a.r.87.v.35.x.2.0.0.f
L|Warren Tryon|R|Capitol Counsel LLC|e0|a5|jx|2m.o7.7a.oq.0.3jt.1b.33.h.2fm.29.14a.cf.1.1.0.0.1
L|Joshua Hurvitz|D|NVG, LLC|71|ai|jx|2n.nw.bs.ok.0.3gy.q.2u.d.qb.1v.7a.23.1.0.0.1y.0.0.0.0.1
L|VEN Neralla|D|Federal Street Strategies, LLC|9i|cn|jw|2o.ns.dp.p4.0.30k.q.19.6.5s.u.1m.1.4.0.0.5.0.0.0.0.1.0.0.0.w
L|Shannon Finley|D|Capitol Counsel LLC|b9|8b|jv|2p.o1.9o.op.0.4sp.20.4v.h.yw.u.183.1q.0.0.0.2j.1.0.1.0.1
L|Emily Murry|R|Tarplin, Downs & Young, LLC|i6|a8|jv|2q.p8.p.pw.0.5u2.27.2a.c.ks.u.7d.25.2
L|Norm Coleman|R|Hogan Lovells Cadwalader US LL|kg|99|ju|2r.mw.tb.no.c.4f9.1h.o.v.44.9.3m.j.0.0.2
L|David Thomas|D|Mehlman Consulting, Inc.|8k|7t|ju|2s.p0.15.pw.0.3ny.4i.dt.14.wg.22.op.3h.0.1.0.z.0.1
L|Matthew Johnson|R|Klein/johnson Group|gd|b2|jt|2t.ov.1n.pn.0.31q.1h.29.x.we.w.1lz.5o.1.0.0.a.1
L|Elizabeth Maier|R|Brownstein Hyatt Farber Schrec|fz|7p|jt|2u.o0.a9.nz.0.31e.19.28.q.6o.y.9d.3i.1.0.0.0.3
L|Scott Gelbman|D|K&L Gates, LLP|7o|9u|jt|2v.p0.19.pb.0.2sb.26.2w.12.az.18.8q.30.1.0.0.p.0.0.0.0.2
L|Andrew McKechnie|R|Tiber Creek Group|k0|ba|js|2w.ne.k6.oa.0.3m3.p.26.7.ec.k.32.w.2.0.0.0.0.1.0.1
L|Kristina Dunklin|R|Forbes-Tate|e8|bz|js|2x.ns.dx.pc.0.3lj.1u.38.g.80.m.16.a.2.0.0.2
L|Robert Babcock|R|Axadvocacy Government Relation|ju|9l|jr|2y.nx.bh.oj.0.3xj.1c.3m.f.na.u.91.2o.2
L|Natalie Farr Harrison|R|Avoq, LLC|kv|b5|jr|2z.o1.9x.ok.0.3bk.1l.1b.l.13a.1e.lk.3p.4
L|Marc Numedahl|D|Crossroads Strategies, LLC|cj|62|jq|30.nk.hi.p7.0.3kh.1w.5b.12.8m.d.19.5.2
L|Ashli Scott Palmer|D|Resolution Public Affairs, LLC|8y|8k|jq|31.o4.8t.p0.0.36k.10.1q.5.7q.b.2o.e.1.4.0.0.0.0.0.0.3
L|Matthew Leffingwell|R|Tiber Creek Group|f1|7c|jq|32.nc.lk.o3.0.38y.10.2p.c.cg.h.37.17.3
L|Jonathan Kott|D|Capitol Counsel LLC|bf|bj|jq|33.mh.114.nw.0.254.y.g.9.20.a.z.4.5.0.0.k.1
L|MJ Kenny|D|Kountoupes Denham Carr & Reid|8u|76|jp|34.ny.b3.p9.0.44e.16.1s.o.5f.l.8e.5.1.0.0.14
L|Michael Long|D|S-3 Group|bm|8g|jp|35.nv.cf.ov.0.2pk.10.m.2.58.l.ae.f.1.1.0.5y.0.0.0.1
L|SAM Olswanger|R|Akin Gump Strauss Hauer & Feld|kt|8z|jp|36.ps.3.qb.0.7z9.35.5n.15.2d2.1r.ju.an.0.2.0.0.1
L|Philip English|R|Arentfox Schiff LLP|ir|cv|jp|37.mw.t7.n2.0.167.x.41.x.uo.1w.ae.5u.0.0.2.5.1
L|Greg D'angelo|R|The Nickles Group, LLC|i8|92|jp|38.ne.kh.nw.0.319.s.35.h.7o.i.8a.22.0.3.0.2.0.0.1
L|Elizabeth Greer|D|Forbes-Tate|c7|9c|jp|39.o6.7w.oq.0.5g8.29.2x.f.mi.1e.e6.57.1.0.0.5.1.0.0.0.1
L|Lori Denham|D|Kountoupes Denham Carr & Reid|9s|9n|jp|3a.o7.7b.or.0.3qf.13.12.c.1mx.23.1mp.66.1.0.0.k.0.0.1.1
L|Daniel Ziegler|R|Williams And Jensen, PLLC|i3|b3|jp|3b.ol.2y.oz.0.27j.1r.14.n.e6.n.7c.27.2.0.0.a
L|Charlotte Ivancic|R|Tarplin, Downs & Young, LLC|iv|9v|jp|3c.nu.cp.of.0.6uv.2c.2b.c.d4.g.5c.k.2.0.0.0.0.0.0.0.3
L|Alexander Perkins|D|Mehlman Consulting, Inc.|an|69|jp|3d.ny.b1.pi.0.4ui.4h.dr.15.6q.x.12.g.1.0.0.2.0.1
L|Oscar Ramirez|D|Fulcrum Public Affairs LLC|6l|b0|jp|3e.os.20.pl.0.2k8.1f.9.h.1m3.1k.en.4r.3.0.0.17
L|James Moran|D|Moran Global Strategies, Inc.|7f|6k|jp|3f.o1.9k.o2.0.2bk.c.0.1.ow.14.74.1u.0.0.2.3h.2.1.0.0.0.0.0.0.2
L|Christopher Matthiesen|D|Federal Hall Policy Advisors|50|48|jo|3g.ny.ax.pb.0.4ln.1c.19.g.6t.f.28.f.3.0.0.0.0.0.0.0.1
L|Brian Greer|D|Empire Consulting Group|at|7s|jo|3h.oi.3h.pq.0.2zi.y.k.m.16o.1l.3w.q.4.0.0.0.0.1
L|Michael Williams|D|Forbes-Tate|74|bp|jo|3i.no.fe.p7.0.47b.24.2z.i.5z.f.z.c.2
L|Shimon Stein|R|S-3 Group|kf|af|jo|3j.oe.4k.p6.0.29l.1o.1i.e.kc.x.6i.2s.2.0.0.0.1
L|Melissa Edwards|R|Missy Edwards Strategies, LLC|g8|al|jo|3k.mu.tu.nx.0.348.e.6h.4.a6.e.8g.2.1.0.0.0.0.3
L|Helen Tolar|R|Mehlman Consulting, Inc.|ef|5z|jo|3l.nx.bq.p0.0.3hz.4d.df.15.50.f.2x.r.1.1
L|Jason Gleason|D|Crossroads Strategies, LLC|az|7z|jo|3m.np.f3.oa.0.4wg.2u.7r.y.9v.h.6j.2f.1.1
L|Russell Sullivan|M|Brownstein Hyatt Farber Schrec|d6|bq|jo|3n.ol.2u.ot.0.7f4.2q.19.x.nc.1j.8h.31.0.1.0.k.1.1.0.0.3
L|David Schwietert|R|Akin Gump Strauss Hauer & Feld|kd|7y|jn|3o.o1.9w.oi.0.2xv.16.1a.l.2s.c.3q.v.1.0.0.0.0.0.8
L|Jennifer Olson|R|Tiber Creek Group|jo|8b|jn|3p.n7.nu.o4.0.544.1d.2q.c.6j.f.4q.e.1.0.0.0.1.1
L|JAY Sulzmann|R|Penn Avenue Partners|k1|a4|jn|3q.nr.e3.oe.0.4by.1a.2q.w.a8.x.8m.1s.2
L|Caitlin VAN Sant|D|Mehlman Consulting, Inc.|8h|88|jn|3r.mq.vu.nt.0.33z.3w.d6.13.54.n.1x.a.1.0.0.p
L|Tripp McKemey|R|Brownstein Hyatt Farber Schrec|kz|74|jn|3s.oa.5u.p6.0.2xq.1v.1c.y.66.16.1o.i.3
L|John Steitz|R|Ridgeline Advocacy Group LLC|l8|8y|jm|3t.op.2j.pk.0.347.1g.1e.x.lv.s.dg.2i.2.1
L|Benjamin Klein|D|Invariant LLC|9c|c7|jm|3u.ol.30.on.0.3vz.1k.3h.w.sh.1f.p1.3z.1.0.0.a
L|Olivia Kurtz|R|S-3 Group|ig|8k|jm|3v.o2.9d.p9.0.5tl.1k.z.5.6a.b.1p.15.3
L|Edward Royce|R|Brownstein Hyatt Farber Schrec|h5|97|jk|3w.of.41.ok.0.2yh.1a.8.13.1xz.2p.7p.3t.0.0.2.0.1.1
L|Christopher Buki|R|S-3 Group|le|bn|jk|3x.nn.g9.o8.0.2it.23.1w.e.q4.1q.7e.1w.3
L|Christopher Wilcox|D|Williams And Jensen, PLLC|a4|8h|jk|3y.o4.8d.ob.0.3s6.1q.3t.l.a7.z.1fg.1y.1.1
L|Dennis Cardoza|M|Foley & Lardner LLP|5v|a5|jk|3z.og.3s.of.4.2m5.1e.4.b.1z4.4j.7n.38.0.0.2.1y
L|Jeffrey Strunk|R|Forbes-Tate|ga|cl|jk|40.nl.gy.o4.0.3cl.1p.2y.8.b9.i.5k.3d.2
L|Jeffrey Carroll|D|Capitol Counsel LLC|bx|8u|jj|41.ok.36.py.0.576.21.40.l.lw.1a.1k.14.1.0.0.0.1.0.0.0.1
L|Margaret Joseph|D|Tarplin, Downs & Young, LLC|as|bg|jj|42.l1.1wh.lz.0.4be.1w.2l.c.f.3.k.0.3.0.0.0.0.1.0.0.1
L|Joseph Eannello|R|Capitol Counsel LLC|hd|bb|jj|43.mt.ur.o2.0.4i6.21.41.m.5k.k.i.q.2.0.0.0.0.0.0.0.0.0.1
L|Benjamin Quayle|R|Venture Government Strategies|j4|c0|jj|44.mu.tv.o4.0.3rf.y.20.n.8m.j.u.e.0.0.2
L|Joseph Britton|D|Pioneer Public Affairs|ad|d7|jj|45.ol.2w.pi.0.2kd.l.a.8.us.1e.7b.1y.3.0.0.p.0.0.0.0.0.0.0.1
L|Ivelisse Porroa-Garcia|D|Crossroads Strategies, LLC|aq|ef|jj|46.n4.ow.oe.0.2sp.1q.6o.10.22.i.d.0.2
L|Gordon Bates|R|Akin Gump Strauss Hauer & Feld|c0|a0|jc|4s.pb.j.ps.0.35a.13.3c.q.164.1r.k6.26.1.0.0.0.1
L|Carlisle Clarke|R|VAN Scoyoc Associates|mf|91|jb|4x.nq.ea.o2.c.2kb.s.2s.9.hs.s.6i.16.1
L|Daniel Farmer|D|BGR Government Affairs|8b|ah|j4|5v.pg.a.q2.0.5y1.20.d.m.wc.1e.go.2m.2.0.0.5.0.0.0.0.2
L|JON Porter|M|Porter Group, LLC|fc|8n|j2|69.lv.1ei.m2.c.qa.e.7.9.z1.v.5b.10.0.3.2.1u.0.1
L|William Wichterman|R|Covington & Burling LLP|m8|4j|ip|87.mp.wl.ms.6.37r.a.e.h.1y.4.2q.y.1.0.0.0.4
L|Mark Warren|R|Brownstein Hyatt Farber Schrec|g7|de|il|8q.pi.8.py.0.5xr.27.13.z.je.1f.a1.4v.1
L|Erskine Wells|R|BGR Government Affairs|kh|a1|ii|96.pl.5.q4.0.5u4.1u.0.u.1bt.1m.18c.66.1.2.0.0.2
L|Ryan Leavitt|R|Barker Leavitt, PLLC (SKA MR.|mm|5q|ia|b3.n2.py.p8.c.32j.m.1.l.a0.d.5.3.5
L|Chris Jahn|R|American Chemistry Council|ft|5t|i8|bf.mi.10f.ls.c.4yk.1.64.u.p.1.6e.55.0.0.0.0.0.0.0.0.0.5.0.1
L|Remy Mason|D|BGR Government Affairs|cl|9v|i8|bn.pg.b.q2.0.5jt.1y.5.q.js.1g.j8.2k.2.0.0.0.0.0.0.0.1
L|Robert Goodlatte|R|Goodlatte Group, LLC F.k.a. Ro|ok|fe|i7|bx.k7.2el.n7.8.1g3.5.27.7.be.1y.0.0.0.0.2
L|Joseph LAI|R|BGR Government Affairs|kk|cb|i3|d1.pf.d.pw.0.4ay.1k.0.q.sb.10.1d2.6p.1.3.0.0.1.0.0.0.1
L|Collin Peterson|M|The Peterson Group Inc|h8|ax|i0|dd.k2.2h2.m4.c.r2.c.26.3.nr.19.p.0.0.0.2
L|Tola Thompson|D|Ballard Partners|5s|ca|hz|dv.lp.1i6.mu.4.2fu.18.2.u.2c.8.1t.1.1.1.0.p.1.0.0.0.1
L|Kate Hull|R|Fierce Government Relations|il|87|hy|e3.nw.cc.ok.4.4i5.2f.9j.x.mk.p.8r.1s
L|TED Lehman|R|Todd Strategy Group|i3|c1|hw|ej.q0.1.ps.0.3yy.22.1y.d.m6.w.ds.2q.0.1
L|SYD Terry|D|BGR Government Affairs|b3|e0|ht|ey.pd.g.pz.0.3qb.1g.1.r.ts.1t.a8.2g.2.2
L|Jonathan Heafitz|R|Pharmaceutical Care Management|mb|9z|hl|hd.pd.f.oy.0.7x8.1.4j.6.1cc.3o.eq.4o.0.0.0.a.0.0.0.0.0.0.0.1
L|Carlos Trujillo|R|Continental Strategy, LLC|go|4h|hi|i5.oo.2l.ob.g.9b2.26.0.y.eh.9.k8.53.0.0.0.0.1.1.0.0.0.0.1
L|James Brandell|R|John Hancock Life Insurance Co|lp|3h|hh|ig.mc.145.m8.4.1l4.i.1c.k.30.6.14.13.1
L|Scott Mason|U|Holland & Knight LLP|mr|6l|hb|ki.lc.1p5.kw.g.1l4.p.1b.i.h.3.2o.1b.0.0.0.0.1
L|Shawn Donilon|R|National Association Of Broadc|ip|dq|h1|oh.pw.2.pj.0.4ls.1.2b.4.8w.d.7x.2i.0.0.0.0.0.0.0.0.1.0.0.1
L|Shannon Kellogg|R|Amazon.com Services LLC|ka|8f|gx|pq.na.m6.my.o.1mo.1.1w.t.62.i.69.2p.0.0.0.0.0.0.0.0.7
L|John Leganski|R|Harbinger Strategies, LLC|ln|6a|gx|pv.lo.1ig.mq.1.5lw.20.3k.d.u.5.p.8
L|Timothy Costa|R|Continental Strategy, LLC|jx|c3|gx|pz.od.4o.pf.8.556.14.0.v.8u.d.1w.k.1
L|Natalie McIntyre|R|Miller Strategies, LLC|be|6h|gs|s4.lj.1kx.n0.4.1kx.v.5.w.1t.4.a.3.2
L|Travis Lucas|R|Lucas / Compton|kx|fp|gr|sl.o6.7p.op.c.28i.d.0.1.dy.8.48.1g.1
L|Matthew Haller|R|International Franchise Associ|nx|5z|gk|w6.la.1qh.k6.c.19u.1.14.5.p.1.46.2f.0.0.0.0.0.1.0.0.0.2.0.3
L|Leslie Belcher|M|Steptoe LLP|hb|7n|gi|x2.po.4.pw.0.3mh.v.1.m.ve.27.cb.1e.0.0.0.f.1
L|Tracie Pough|D|Ballard Partners|58|7t|g4|13x.lo.1ij.n9.8.1fl.t.2.n.20.a.f.1.1.0.0.0.1
L|Truman Reed|R|Akin Gump Strauss Hauer & Feld|du|er|g0|16a.gk.4n7.fl.8.1d1.10.d.n.0.0.b.6.2.2
L|Rick Zampelli|R|Cornerstone Government Affairs|k9|ej|fz|16o.mp.w3.nn.c.24o.18.6.i.9q.u.1g.n
L|Scott Kamins|R|Kamins Consulting|pd|fi|fy|177.lh.1mb.mh.o.1vx.a.9.3.2c.8.9.2
L|Terry Campbell|R|Nasdaq, Inc.|gc|7k|fx|17r.mi.10u.m1.c.2c2.1.o.3.z.4.34.21
L|Christopher Lacivita|R|Checkmate Government Relations|h2|dw|fw|18a.kp.246.lz.x.8bu.37.3.15.u.1.2.7.0.0.0.0.0.0.0.0.0.0.0.0.p
L|Paul Richman|D|Insured Retirement Institute|46|4q|fu|1a0.l6.1tc.k3.4.10o.1.5n.5.f.3.u.q.0.0.0.0.0.0.1.0.0.0.0.1
L|Matthew Forck|M|Ameren Services|q4|8a|fq|1c6.n0.r3.mh.4.2l7.1.y.1.19.6.4t.25
L|Joseph Devooght|R|Textron Inc.|cy|5i|fq|1c7.mm.y1.m3.c.2ur.1.0.0.w.3.3u.1v.1
L|Michael Galano|U|Holland & Knight LLP|kq|6y|fo|1dm.gb.4ui.eq.c.1sg.f.17.h.0.0.z.g.0.0.0.0.2.0.0.0.5
L|Jameel Aalim-Johnson|D|Nasdaq, Inc.|5z|98|fn|1du.n7.nh.mz.6.2c2.1.o.3.4c.6.41.1l
L|Theodore Okon|R|Community Oncology Alliance|3p|eq|fl|1f6.pc.h.ox.0.5d9.1.7.2.1w0.24.46.23.0.0.0.0.0.0.0.0.0.0.0.1
L|Craig Carbone|R|Continental Strategy, LLC|cf|30|fj|1g4.lm.1jn.m0.4.2on.q.0.m.a.1.4g.2.1
L|William Walters|R|Select Medical Holdings Corpor|cn|ee|fe|1j8.pe.e.ow.0.5k0.1.0.1.2n4.18.64.29.0.0.0.a.0.1.0.0.0.0.0.0.2s
L|Robert Porter|R|Capitol Hill Policy Group LLC|jr|fo|ev|1xh.j2.308.mb.2.1bf.d.22.o.5u.8
L|Cameron Krier Massey|M|Cameron Krier Massey, Inc. DBA|i2|es|es|1zp.h7.43i.jv.c.ku.2.u.9.28.3.0.0.1
L|Kent Hance|R|Hance Scarborough|ka|ce|er|20o.ln.1iw.lc.c.hs.e.5.c.we.14.zb.92.0.0.0.a
L|Mike Carr|D|Boundary Stone Partners|pi|4l|eq|213.lg.1n7.lv.6.1v1.i.2.l.14.5.28.3.0.1
L|JOE Ellis|R|BGR Government Affairs|i0|fb|en|23v.ma.160.m8.4.ry.l.0.f.3m.6.33.17.1
L|Michael Doyle|D|K&L Gates, LLP|5b|e5|ed|2c9.ke.2a2.jr.c.i8.f.j.j.1m.6.1t.14.0.0.1
L|George Sorial|R|Javelin Advisors LLC|p9|ed|ec|2d2.id.3ed.le.c.1e0.9.0.a.2i.2.0.0.0.0.0.0.3
L|Thomas Kahn|D|The Cormac Group, LLC|ai|cs|e9|2f7.l3.1v6.l7.c.gx.a.e.6.rz.y.sx.b.0.0.0.0.0.0.0.0.8
L|Peter Grollman|M|The Children's Hospital Of Phi|fv|du|e4|2k0.k2.2gt.kh.c.o4.1.x.7.2d.6.1r.4
L|John Tanner|D|Bridgeway Advocacy|l1|2f|e4|2k2.g6.4yz.ih.2.gs.6.1.2.k.2.0.0.0.0.2.0.3
L|Paul Feenstra|D|Paccar Inc|cc|45|e2|2lr.ky.1yb.kz.c.1sq.1.1.g.k.2.k.a.0.0.0.0.0.0.1.1.2
L|Laramie Adams|U|Texas Farm Bureau|es|gx|dv|2rc.gm.4l5.f5.o.2dz.1.7.0.0.0.i.7.0.0.0.0.0.0.0.0.1.0.0.1
L|Todd Askew|U|American Medical Association|p5|3f|du|2se.eb.6hi.f8.c.2kn.1.cv.16
L|Lori Laudien Ziebart|M|Ziebart Consulting, LLC|lv|9q|ds|2u4.k6.2ex.lr.c.nc.1.c.2.z2.m.5.0.0.0.0.0.0.0.0.0.0.0.0.1
L|Matthew Shapanka|U|Covington & Burling LLP|96|68|dr|2vd.jm.2pu.jy.4.1fz.2.9.a.4.3.i.0.0.0.0.0.0.0.0.0.1.0.0.0.2
L|Wayne Pacelle|M|Animal Wellness Action|82|84|dp|2wg.l5.1tw.kb.8.94.1.1c.c.1sw.42.2s.24.0.0.0.0.0.0.0.0.0.0.0.1
L|Thomas Fletcher|R|Blue Cross And Blue Shield Ass|n2|81|dh|34t.do.74e.eb.4.q4.2.ax.7.0.0.0.0.1.0.0.0.0.0.0.0.2
L|Brad Close|U|Nfib (National Federation Of I|c0|2h|dg|35p.e1.6r6.ew.8.1zx.2.4e.d
L|Kevin Conlon|D|Conlon Public Strategies|3v|4w|de|37i.lj.1l3.lb.2.jq.6.0.b.hs.p.95.2s.0.0.0.u.0.0.0.0.3
L|Christopher Kearney|U|The Ferguson Group, LLC|ja|g3|dc|39g.dg.7ch.ev.c.1y8.t.19.n
L|Regan Beck|U|Texas Farm Bureau|fs|hl|d9|3bu.go.4iv.f5.c.2dz.1.5.0.0.0.l.8.0.0.0.0.0.0.0.0.0.0.0.1
L|Natalie Torentinos|U|National Association Of Childr|fm|fe|d8|3d3.dz.6tr.f5.c.2ej.1.2b.g.0.0.0.0.0.0.0.0.0.0.0.1
L|MAX Richtman|U|National Committee To Preserve|dl|gc|d4|3ha.dz.6ts.cv.14.nu.1.4t.c.0.0.1.0.0.0.0.0.0.0.0.0.0.0.0.1
L|Kelly Bobek|U|Volvo Group North America, LLC|l2|gk|d0|3ln.fa.5o0.dn.c.zf.1.1f.6.0.0.f.6.0.0.0.2.0.0.0.0.1
L|VIN Weber|R|Mercury Public Affairs, LLC|n9|93|cy|3n6.hi.3w5.ka.c.hj.5.d.3.5d.6
L|Patrick Flood|R|Cornerstone Government Affairs|kk|8q|cp|3wx.ka.2ce.ks.8.me.h.1.a.3h.e.p.c
L|Anthony Wilkinson|U|National Association Of Govern|oy|av|ch|465.dh.7bx.e7.o.1bd.1.12.2
L|Mike Conaway|U|Conaway Graves Group, LLC|qd|a6|c3|4lp.c5.8yu.d3.c.qh.9.2.1.0.0.0.0.0.0.2
L|Haley Olchyk|U|Nextera Energy, Inc.|y|eh|by|4rq.eq.63t.fl.c.3m0.1.0.j.0.0.0.0.0.0.0.0.0.0.1
L|Manuel Espina|U|Continental Strategy, LLC|g4|he|bu|4w1.dv.6xu.f0.o.26b.9.0.4
L|Steve Stivers|R|Ohio Chamber Of Commerce|im|e2|bh|5b6.hz.3lk.g5.4.0.1.4.5.c6.g.6f.22.0.0.2
L|Jamie Dangers|U|Susan B Anthony List|nr|l|bd|5ex.c9.8u3.cj.c.jy.1.8d.2.0.0.0.0.0.1
L|Sean McCarty|U|Helena Agri-Enterprises, LLC|l3|1v|bd|5f4.gi.4o4.iy.c.11i.1.0.2.5.1
L|Jeff Duncan|U|Covenant Government Affairs, L|ac|ei|as|61c.h4.45l.h5.4.9v.a.0.9.a.2.8.4.0.1.1.0.0.0.0.0.0.0.1
L|Mark Bowersox|U|Manufactured Housing Institute|nc|g3|aa|6m0.f2.5ud.br.c.d2.1.2.c.0.0.57.35.0.0.0.0.0.0.0.0.0.0.0.1
L|Maryanne Dunlap|U|Chattem, Inc D/b/a Opella|oj|ec|a2|6ua.cj.8gg.dn.c.z0.1.8.1
L|Denise Edwards|U|National Children's Alliance|r7|23|9t|750.d2.7t2.ec.c.1eu.1
L|Heather Ansley|U|Paralyzed Veterans Of America|br|49|9b|7q1.a0.cbo.aa.c.50.1.iy.j.0.0.0.0.0.0.0.0.0.0.2.0.b.1.1.1
L|Steve Symms|U|Parry, Romani, Deconcini & Sym|oq|8l|99|7ro.bv.9cg.ca.8.h8.5.0.1.0.0.0.0.0.0.0.0.2.1
L|Laura Hall|D|Bipartisan Policy Center Actio|r|5l|97|7tu.by.98o.cu.4.ni.1.0.0.0.0.0.0.1.0.0.0.0.0.0.0.0.0.0.1
L|Tiernan Sittenfeld|U|League Of Conservation Voters|61|h8|93|7yr.bq.9kw.bs.4.5g.1.80.u.0.0.0.0.0.0.0.0.0.0.0.0.0.0.0.1
L|LIZ Clark|U|International Health Racquet &|60|89|92|7z4.cm.8co.b4.o.8w.1.6.0.0.0.9.4.0.0.0.0.0.0.0.0.0.0.3
L|Mini Timmaraju|U|Reproductive Freedom For ALL|p|5q|91|80u.bf.a1f.9r.4.3b.1.4a.d.0.0.w.0.0.0.0.p
L|Alisa Casavant|U|Arthritis Foundation|5x|o|8m|8g5.b6.aea.bu.c.dk.1.n.8
L|David Bradley|U|David A. Bradley|b2|h4|89|8ul.c0.96b.cx.c.o9.1.0.0.0.0.0.0.0.0.0.0.0.0.0.0.0.0.1
L|JT Young|U|Ford Motor Company|lm|1x|83|90k.bu.9e4.c0.o.eu.1.0.e
L|Daniel Zimmerman|U|Boundary Stone Partners|at|3q|7z|94e.be.a3g.c3.4.fp.b.4.a.0.0.0.0.0.0.0.0.0.0.0.0.0.0.2
L|Josh Winegarner|U|Texas Cattle Feeders Associati|fd|hf|7w|97x.b9.aah.b1.c.8c.1.d.f
L|Monica Reid|U|National Fair Housing Alliance|ov|33|7s|9c2.am.ba3.b2.c.8o.1.d.2.0.0.0.0.0.0.0.0.0.0.1
L|TOM Luce|U|TOM Luce Consulting|nt|bo|7h|9nn.ed.6f4.g2.4.32.1.0.0.k.3
L|Fred Wertheimer|U|Democracy 21|5d|4o|7g|9pr.a9.bve.am.c.6e.1.12.e.0.0.0.0.0.0.0.0.0.0.0.0.2
L|Dustin Bryant|U|The Texas A&M University Syste|c3|g8|7a|9wc.ax.ast.bh.c.b5.1.5.1.0.0.0.0.0.0.0.0.0.0.0.0.2
L|Ryan Whitehouse|U|Illinois Agricultural Associat|78|40|72|a3v.ci.8im.aq.8.6w.1.0.2.0.0.2.0.0.0.0.0.0.0.0.0.1
L|Zachary Hartman|U|Ducks Unlimited, Inc|lt|1o|60|b7x.a7.bzr.aj.c.60.1.2.7.0.0.0.0.0.0.0.0.0.0.0.0.0.0.0.1
L|Katy Button|U|Georgetown University|eg|ha|5u|be8.bp.9mk.ci.c.0.1.0.0.2.1.0.0.0.0.0.0.0.0.1
L|Francis Bradley|U|Electricity Canada (Formerly K|mx|go|5r|bgk.ag.bjy.av.c.7l.1.0.3
L|ROB Wallace|U|ROB Wallace Group, LLC|pk|f4|5e|btj.am.b9g.b3.4.8r.1.0.2
L|Steven Winberg|U|Net-Negative Co2 Baseload Powe|ox|ak|4s|cf3.9z.cdp.9x.c.3r.1.0.0.0.0.c
L|DAN Stein|U|Federation For American Immigr|r4|fu|44|czc.8j.eya.8a.c.d.1.e.0.0.0.0.0.0.1.0.0.0.0.0.1
L|Thomas Porter|U|Iraq And Afghanistan Veterans|m|2b|3t|d95.8h.f0l.88.o.a.1.9.2
L|Nikki McKinney|U|Democracy Forward|2w|21|3q|db9.91.e3f.8y.e.1e.1.1
L|Bill Woolf|U|Woolf Strategic Solutions Grou|nm|eq|2o|e9l.8c.f9x.81.c.3.4
`;
const RSC = `
L|Patricia Miller|U|American Wild Horse Campaign|hp|gp|2d|ejc.8i.ezm.89.c.b.1.0.4
L|Garrett Harencak|U|Harencak Consulting|63|6e|1o|f3s.7z.g0p.7k.c.0.1
K|American Petroleum Institute|U||df|a4|oq|1.nzw.60.3b.b6s.1v.9.0.0.0.6.7.t
K|National Association Of Realtors|U|501(c)(6)|ap|c4|oe|2.5g40.4r.2u.moy.5.5.0.0.0.0.0.15
K|American Chemistry Council|U||cj|73|o9|3.1kls.6i.3b.s2.1c.9.0.0.0.1.1.w
K|AFL-CIO|U||76|dv|o8|4.8do.dh.66.1mx.d.7.0.0.0.4.4.n
K|Southern Company|U||it|90|o3|5.13f1.16.v.2s.k.5.0.8.d.0.0.g
K|American Fuel And Petrochemical Manufacturers|U||b6|c5|nm|6.w6w.1x.19.gj.11.4.0.0.0.2.2.4
K|Johnson & Johnson|U||ds|au|nj|7.w80.2u.1l.35.9.1.0.g.i.8.9.e
K|American Civil Liberties Union|U||7l|dq|nj|8.6gd.fo.6j.a0.6.j.0.0.0.1.1.18
K|Association Of American Railroads|U||e4|ay|nj|9.hb3.3l.22.rs.3.d.0.0.0.1.1.4
K|Microsoft|U||gw|7x|nd|a.103w.40.29.f.2.6.m.s.10.0.0.y
K|Doordash|U||c5|bu|n6|b.94c.1z.1i.u5.4.1.0.2.0.0.0.f
K|CVS Health|U||bq|9e|n3|c.zdr.1k.x.10y.1.5.0.6.7.6.6.7
K|League Of Conservation Voters|U|501(c)(4)|83|fv|n1|d.33e.a6.4w.1gn9.b.0.0.0.0.0.0.v
K|International Association Of Fire Fighters|U||bh|cz|mo|e.2av.4t.34.up.2.9.0.0.0.2.2.x
K|General Motors|U||cr|9g|mh|f.1mf2.26.1f.64.3.0.0.1.3.0.0.i
K|National Nurses United|U||4m|c8|mf|g.1va.3k.20.5o1.4.1.0.0.0.3.3.g
K|American Federation Of Teachers|U||7i|e6|mc|h.4ce.gu.6v.7n.3.2.0.0.0.0.0.j
K|Elevance Health, Inc.|U||f3|bi|mb|i.pf5.2c.19.8k.1.3.0.4.2.2.2.7
K|Pfizer Inc|U||bb|9s|m9|j.169t.2i.1i.2x.2.0.0.e.e.5.5.g
K|Valero Energy Corporation|U||iy|db|m7|k.9om.n.i.6y.5.0.0.4.1.0.0.c
K|American Federation Of State County And Municipa|U||7a|f1|m6|l.7gw.e8.5x.6yf.2.0.0.0.0.0.0.2
K|Altria Client Services LLC|U||cm|bf|m5|m.1cx8.1q.11.ghk.2.0.0.0.0.1.1.c
K|American GAS Association|U||js|6i|m2|n.4fg.1h.y.u.7.a.1.0.0.1.1.7
K|American Exploration & Production Council|U||k6|di|ln|o.659.1h.w.2s.a.1.0.0.0.0.0.a
K|Duke Energy Corporation|U||ho|80|lm|p.qxq.48.2d.0.8.5.0.1.c.0.0.i
K|United Airlines, Inc.|U||c9|7o|ll|q.jf6.16.t.1c.4.1.0.1.1.0.0.8
K|Meta Platforms, Inc.|U||jb|6y|ll|r.2711.2y.1s.4v.0.2.0.11.x.0.0.s
K|Communications Workers Of America|U||8w|3b|lk|s.5hz.3a.1z.dmv.0.5.0.0.0.1.1.i
K|Safari Club International|U||my|c8|li|t.370.m.f.3v.4.3.0.0.0.0.0.4
K|National Education Association|U||7u|ee|lh|u.95g.cm.5b.b9.2.0.0.0.0.3.3.g
K|Intel Corporation|U||gx|6t|lh|v.hyy.1m.12.5.5.2.0.d.a.0.0.i
K|National Community Pharmacists Association|U||b0|7h|lg|w.4lc.30.1k.rs.1.3.0.0.0.0.0.i
K|Biotechnology Innovation Organization|U||8n|9p|lg|x.r9j.7i.3f.p.3.3.0.0.0.4.5.q
K|Poet LLC|U||h0|cc|lg|y.bx1.15.n.el.3.0.0.0.0.1.2.e
K|The Boeing Company|U||eu|6x|le|z.15i6.38.1u.0.5.3.0.g.h.0.0.u
K|Federation Of American Hospitals|U||bn|e3|lb|10.bj6.2t.1k.m.5.0.8.0.0.a.c.5
K|Coinbase, Inc.|U||al|dd|l9|11.fff.l.i.29wt.0.9.0.0.0.1.1.e
K|Delta AIR Lines|U||dw|b8|l8|12.lww.3o.26.z.3.0.0.1.1.1.1.p
K|Vertex Pharmaceuticals|U||em|bd|l5|13.h9y.16.v.8c.1.0.0.4.4.3.3.e
K|The Home Depot|U||cx|8q|l4|14.cd0.1p.16.1e.0.5.0.t.w.1.1.r
K|Human Rights Campaign|U||fe|7b|l4|15.2s7.em.4x.r.4.2.0.0.0.1.1.l
K|Airlines For America|U||hx|8r|l2|16.4me.1s.16.a.d.c.0.0.0.2.2.9
K|American Property Casualty Insurance Association|U||fg|9i|l0|17.lf6.bb.5d.d7.0.4.0.0.0.0.0.d
K|Bristol Myers Squibb|U||er|b0|kx|18.sma.1w.16.a.5.0.0.5.4.6.7.4
K|American Israel Public Affairs Committee|U|501(c)(4)|b7|43|kx|19.9nh.7o.32.vmw.0.1.0.0.0.0.0.8
K|Service Employees International Union|U||7k|8i|kv|1a.1cm.h.d.8w.4.2.0.0.0.2.2.1
K|GUN Owners Of America Inc|U||8a|4d|ku|1b.6q3.fc.5n.109.0.2.0.0.0.0.0.4
K|Xcel Energy Inc|U||k7|6s|kt|1c.74e.6z.35.0.6.2.0.2.4.0.0.4
K|National Mining Association|U||e2|5p|ks|1d.9bx.7t.38.0.16.6.1.0.0.1.1.n
K|Wells Fargo & Company|U||66|8s|kq|1e.e05.k.f.32.0.3.0.7.f.0.0.b
K|Edison Electric Institute|U||g0|80|ko|1f.xlw.6l.3s.0.v.7.0.0.0.1.1.b
K|National Association Of Manufacturers|U||8s|6l|kn|1g.quq.32.28.0.g.k.0.0.0.5.5.1p
K|American Hospital Association|U||ej|85|km|1h.23im.7q.3e.0.e.7.0.0.0.b.d.r
K|Laborers' International Union Of North America|U||ia|3i|kl|1i.4zg.11.p.858.0.2.0.0.0.3.3.8
K|International Brotherhood Of Teamsters|U||b9|4u|kk|1j.4bb.51.33.1e.1.9.0.0.0.1.1.c
K|Advanced Micro Devices (AMD)|U||ea|8g|kk|1k.dgg.i.c.rs.0.1.0.i.h.0.0.n
K|RAI Services Company|U||bg|c6|kk|1l.pxf.k.g.u34.1.0.0.0.0.0.0.c
K|National Association Of Home Builders|U||di|5m|kj|1m.blh.2q.1z.0.j.h.0.0.0.2.2.p
K|National Rural Electric Cooperative Association|U||gb|ff|kj|1n.den.3u.21.0.m.8.0.0.0.0.0.6
K|American Society Of Anesthesiologists|U||77|6z|kj|1o.3hq.2j.1t.5f.1.2.0.0.0.4.4.g
K|Alkermes, Inc.|U||ew|90|kj|1p.f3m.1g.w.1g.2.0.0.1.0.0.0.c
K|Siemens Corporation|U||he|68|kh|1q.cwq.w.m.16.3.1.0.0.0.0.0.10
K|American Trucking Associations|U||hd|57|kh|1r.8ti.a0.4l.0.9.8.0.0.0.0.0.j
K|Davita|U||fn|bg|kh|1s.gqs.z.i.2s.2.0.0.0.1.1.1.7
K|AT&T|U||g5|65|kg|1t.14sy.49.2f.28.0.0.0.r.11.0.0.s
K|Everytown For GUN Safety Action Fund|U||la|dm|ke|1u.7iu.2w.1r.gn8.0.0.0.0.0.0.0.7
K|National Retail Federation|U||7e|63|kb|1v.rfi.3d.22.0.8.4.0.0.0.0.0.z
K|Phillips 66|U||jh|7r|ka|1w.j42.2f.1i.0.i.0.0.5.3.0.0.v
K|Alliance For Automotive Innovation|U||mh|76|ka|1x.ifh.17.u.0.r.b.0.0.0.2.2.g
K|American Forest & Paper Association|U||ha|6k|k9|1y.9h4.21.1i.0.f.5.0.0.0.2.2.g
K|Fedex Corporation|U||ib|5r|k9|1z.14uv.5a.30.0.7.0.0.3.3.0.0.c
K|Environmental Defense Action Fund|U|501(c)(4)|al|eu|k7|20.5kk.1l.13.m9o.0.0.0.0.0.0.0.h
K|Advanced Medical Technology Association (Advamed|U||ec|cd|k7|21.31q.d.9.rs.2.1.0.0.0.1.1.e
K|Council For Innovation Promotion (C4ip)|U||o1|ad|k5|22.1oa.19.t.1hh.0.3.0.0.0.0.0.1
K|American Benefits Council|U||ar|61|k5|23.7bj.4k.2o.0.5.6.0.0.0.3.3.g
K|Unitedhealth Group|U||eo|9x|k4|24.y2y.u.m.q.0.5.0.6.1.7.8.9
K|Juul Labs|U||96|cg|k4|25.7to.b.8.xh.2.0.0.0.0.0.0.5
K|Bank Of America Corporation|U||cr|6b|k2|26.9w4.1a.x.2d.0.0.0.a.12.1.1.9
K|Conocophillips|U||jk|dt|k2|27.n02.1e.x.0.9.0.0.4.5.0.0.h
K|Archer Daniels Midland Company|U||bz|7f|k1|28.ewe.x.k.2s.1.0.0.2.1.0.0.l
K|Amgen|U||dh|9y|k0|29.17t2.41.1y.0.3.0.0.9.c.6.7.7
K|Associated Builders And Contractors Inc|U||66|b3|k0|2a.866.64.3e.0.k.2.0.0.0.1.1.s
K|Charles Schwab & Co., Inc.|U||ld|e0|jz|2b.960.k.e.8s.0.0.0.6.m.0.0.7
K|American Hotel & Lodging Association|U||e7|72|jy|2c.ahb.2h.1o.0.4.5.0.0.0.0.0.j
K|American Airlines, Inc.|U||ht|9r|jy|2d.nmz.1q.15.0.4.1.0.1.3.0.0.g
K|National Pork Producers Council|U||c4|et|jy|2e.70y.1a.t.0.7.8.0.0.0.3.3.d
K|Interstate Natural GAS Association Of America|U||js|6w|jx|2f.5s0.1o.13.0.a.4.0.0.0.2.3.b
K|ELI Lilly And Company|U||c6|cd|jx|2g.y4m.p.j.8.2.1.0.b.6.4.4.9
K|Exxon Mobil Corporation|U||k4|8r|jx|2h.lzo.1b.v.0.4.0.0.5.j.0.0.j
K|National Parks Conservation Association|U||lc|d2|jx|2i.29v.76.3h.0.b.5.0.0.0.0.0.1
K|Consumer Technology Association|U||h9|em|jw|2j.ed0.3y.2n.0.1.7.4r.0.0.1.1.y
S|WinSenate|D|super pac ie only|h1|dj||6at0
S|Defend American Jobs|R|super pac ie only|ed|ey||2lnp.jag
S|NO Going Back PAC Inc.|R|super pac ie only|bc|ei||1ul9
S|Americans for Prosperity Action, Inc. (AFP Actio|R|hybrid pac nonqualified|do|ft||1rbv.azu0
S|Protect Progress|D|super pac ie only|8q|as||znt.jag
S|LCV Victory Fund|D|super pac ie only|ag|fm||xj7.t0as
S|United Democracy Project (UDP)|M|super pac ie only|8n|3u||rbg.hkps
S|WIN IT Back PAC|M|super pac ie only|a8|cv||r53
S|NRCC|R|party qualified|6v|f6||qcl
S|DCCC|D|party qualified|h8|ff||otl
S|Last Best Place PAC|D|super pac ie only|gn|gj||opo
S|Fairshake|M|super pac ie only|7g|cb||i4k.k1g8
S|NRSC|R|party qualified|9u|bn||gdi
S|Duty and Country|D|super pac ie only|ex|f9||flr
S|Lower Costs Now|D|super pac ie only|if|f2||eka
S|AB PAC|D|hybrid pac nonqualified|8r|fz||e68.a4nr
S|A Stronger Michigan|D|super pac ie only|4y|3k||d9n
S|North Star|D|super pac ie only|d2|g4||ceu
S|DSCC|D|party qualified|go|fx||cee
S|Nebraska Values PAC|D|super pac ie only|nu|dh||c8h
S|Your Community PAC|D|super pac ie only|dk|f8||c5a.3m0i
S|FIX Washington PAC|R|super pac ie only|2z|f0||c4w
S|People Over Politics Action Fund|D|super pac ie only|ll|gh||bd7
S|EDF Action Votes|D|super pac ie only|c3|dz||aha.cd7n
S|Safety & Affordability PAC Inc.|R|super pac ie only|9n|e5||afv
S|Club For Growth Action|M|super pac ie only|a0|e8||9vf.b4
S|New Deal for All, Inc.|D|super pac ie only|jp|g7||9gm
S|VoteVets|D|hybrid pac qualified|ce|f3||8an.n5c
S|Accountability Project Inc|R|super pac ie only|j2|39||89o
S|Equality PAC|D|hybrid pac|8k|ac||0.4pz
S|HMP|D|hybrid pac qualified|91|e7||4v5t.wo6y
S|National Association Of Realtors Congressional F|M|super PAC|7x|dk||0.9h1s
S|Communications Workers Of America - Working Voic|D|super PAC|7s|2o||0.6x8h
S|Everytown For GUN Safety Victory Fund (Everytown|D|super PAC|n5|ev||0.98er
S|Laborers' International Union Of North America P|D|super PAC|j8|2t||0.4ac4
S|Make America Great Again Inc.|R|super PAC|8t|f2||0.2oef
S|Maga Inc.|R|super PAC|cg|c1||0.2sb4
S|National Nurses United For Patient Protection|D|super PAC|33|cu||0.31vj
S|SLF PAC|R|super PAC|cz|cx||0.w08c
S|CLF|R|super PAC|9z|ab||0.wzre
S|NHA Action|U|super PAC|9y|ef||0.14ic
S|SMP|U|super PAC|95|ep||0.1px6
S|Neighbor Voices PAC|D|super PAC|5i|g0||0.uv4
S|AFL-CIO Committee On Political Education Treasur|D|super PAC|4h|fa||0.bxi
S|WAY To Lead PAC|D|super PAC|84|2n||0.l7w
S|GOA Victory Fund|R|super PAC|6r|3g||0.k28
S|Organizing Empowerment PAC|U|super PAC|5r|fk||0.hqw
S|Givegreen United Action|D|super PAC|6o|gu||0.k5i
S|FF PAC|D|super PAC|6w|gi||0.1nlso
S|Democracy PAC|U|super PAC|2m|id||0.nkrk
S|Working For Working Americans - Federal|U|super PAC|1h|it||0.a46e
S|Duty To America PAC|U|super PAC|od|iv||0.52eo
S|Climate Power Action|U|super PAC|4x|id||0.2868
S|Blackpac|U|super PAC|5o|hj||0.1r2u
S|FC PAC|U|super PAC|p0|iu||0.1czw
C|NRSC|R|party national committee|ij|ap||1nff.du
C|DSCC|D|party national committee|a3|9f||1ekb.hp
C|DCCC|D|party national committee|9f|9o||t5c.e4
C|NRCC|R|party national committee|hm|a7||gt8.8e
C|Harris Victory Fund|D|joint fundraising committee|4b|4i||b50.hx
C|Johnson Leadership Fund|R|joint fundraising committee|ik|ce||9u6.3t
C|McCarthy Victory Fund|R|joint fundraising committee|l5|9a||81m.3u
C|Trump 47 Committee, Inc.|R|joint fundraising committee|kr|4k||7n1.3l
C|Bhfs-E, PC PAC (Brownstein Hyatt Farber Schreck|M|corporate pac|f0|ap||6i0.2d
C|DNC Services Corp / Democratic National Committe|D|party national committee|3h|c2||5rm.9x
C|Akin Gump Strauss Hauer & Feld LLP Civic Action|M|nonconnected pac|cu|b9||42n.1s
C|Cooper Victory Fund|D|joint fundraising committee|3e|53||3xe.80
C|Emmer Majority Builders|R|joint fundraising committee|n4|8o||3wf.2z
C|Katherine Clark Majority Fund|D|joint fundraising committee|88|8p||3vj.4o
C|Holland & Knight Committee For Effective Governm|M|nonconnected pac|j0|a3||3nv.1r
C|Casey Keystone Victory Fund|D|joint fundraising committee|9k|em||3mg.7r
C|BGR PAC|R|nonconnected pac|gr|dn||3i1.1h
C|Collins Victory Committee|R|joint fundraising committee|kc|7m||3hg.6j
N|Future Forward USA Action|U|501(c)(4)|56|hg||kvbb
N|Democratic Governors Association|U|527 political org|eo|9i||8c08
N|Republican Governors Association|U|527 political org|e9|9h||6ra1
N|Fund For Policy Reform Inc|U|501(c)(4)|3k|hq||5tyc
N|FF PAC|U|grantee|3u|i6||5e24
N|House Majority Forward|U|501(c)(4)|6r|g2||58gy
N|Sixteen Thirty Fund|U|501(c)(4)|7t|gg||548n
N|Stand Together Chamber Of Commerce Inc|U|501(c)(6)|dn|hd||4rzo
N|America Votes|U|501(c)(4)|7b|gn||4mmq
N|Republican State Leadership Committee - RSLC|U|527 political org|f9|a1||3uai
N|ONE Nation|U|501(c)(4)|bp|ey||3myg
N|American Action Network Inc|U|501(c)(4)|4i|a7||3mvf
N|AB Foundation|U|501(c)(4)|73|ha||2usz
N|Americans for Prosperity|U|501(c)(4)|e1|ib||2ld4
N|Jobsohio|U|501(c)(4)|5p|k||2jlc
N|Open Society Action Fund Inc|U|501(c)(4)|5q|gq||2818
N|Republican Attorneys General Association|U|527 political org|cb|dd||203q
N|Democratic Attorneys General Association, Inc.|U|527 political org|cv|dc||1yhv
N|Democratic Legislative Campaign Committee|U|527 political org|9p|dp||1wmy
N|Building America's Future|U|501(c)(4)|om|iv||1rhi
N|Restoration Of America|U|501(c)(4)|89|iw||1ia6
N|Advocacy Action Fund Inc|U|501(c)(4)|67|hb||1e2x
N|Climate Power|U|501(c)(4)|5n|hs||18k9
N|Eastern Atlantic States Regional|U|501(c)(5)|1p|iu||155o
N|North Fund|U|501(c)(4)|98|fr||10lb
N|Global Impact Social Welfare Fund|U|501(c)(4)|a7|gb||zyf
N|American Federation Of State County|U|501(c)(5)|l|gk||z1m
N|HMP|U|grantee|4s|h2||tpg
N|LCV Victory Fund|U|grantee|64|h1||rs0
N|America Votes|U|grantee|3z|i4||qdq
N|Honda Development & Manufacturing Of America LLC|U|grantee|54|l||opt
N|Congressional Leadership Fund|U|grantee|30|a3||lfo
N|AB PAC|U|grantee|65|i5||khi
N|AFSCME Working|U|527 / political org|l|gs||igm
N|American Independent Media|U|501(c)(4)|5t|i3||i4s
N|The Cleveland Clinic Foundation|U|501(c)(3)|6b|k||hv1
N|Americans for Prosperity Action|U|grantee|dg|ib||hlc
N|America Votes Education Fund|U|501(c)(3)|48|i7||euq
N|National Philanthropic Trust|U|501(c)(3)|3r|i2||cxa
N|OUR American Future Action|U|grantee|44|hh||cmk
N|Working America Education Fund|U|501(c)(3)|41|i8||btk
N|American Majority Action Inc|U|501(c)(4)|8z|iw||b0t
N|Floridians Protecting Freedom|U|grantee|6g|hj||asw
N|Campaign for a Family Friendly Economy|U|501(c)(4)|5w|hm||ard
N|NAR Fund|U|527 / political org|6q|e2||ai2
N|Courier Newsroom Inc|U|grantee|4c|ia||ahq
N|Congressional Institute|U|Travel sponsor|l4|86||1
N|Center Forward|U|Travel sponsor|a8|6r||1
N|Conservative Partnership Institute|U|Travel sponsor|mn|fp||0
N|American Israel Education Foundation|U|Travel sponsor|cu|ds||0
N|Global Women's Innovation Network (GlobalWIN)|U|Travel sponsor|6k|71||0
N|Stanford University|U|Travel sponsor|gy|h1||0
N|Third Way Foundation, Inc.|U|Travel sponsor|3o|94||0
N|Republican Main Street Partnership|U|Travel sponsor|it|gh||0
N|Ripon Society and the Franklin Center for Global|U|Travel sponsor|nv|7s||0
N|Animal Wellness Action|U|501(c)(4)|28|5f||0
N|Ducks Unlimited Inc|U|501(c)(3)|ni|n||0
N|Energy Infrastructure Council|U|501(c)(6)|qr|8n||0
N|International Franchise Association|U|501(c)(6)|r3|3q||0
N|Community Oncology Alliance Inc|U|501(c)(6)|p|gf||0
N|National Committee To Preserve Social Security A|U|501(c)(4)|d8|is||0
N|Texas Farm Bureau|U|501(c)(5)|gl|is||0
N|Manufactured Housing Institute|U|501(c)(6)|q6|hx||0
N|Bipartisan Policy Center Action Inc|U|501(c)(4)|o|4b||0
N|Campaign For Sustainable RX Pricing|U|501(c)(6)|3l|3e||0
N|American Council Of Life Insurers|U|501(c)(6)|1w|bu||0
N|American Gaming Association|U|501(c)(6)|l0|hl||0
F|Embassy of the Republic of Korea|U|KOREA, SOUTH|hy|dm||eb.1
F|The Embassy of the Republic of Kazakhstan|U|KAZAKHSTAN|37|53||dp.1
F|Foreign Ministry of Azerbaijan|U|AZERBAIJAN|7k|1e||cd.1
F|Kurdistan Regional Government|U|IRAQ|lz|37||b1.1
F|Administrative Ministry of the Presidency, Domin|U|DOMINICAN REPUBLIC|4z|2l||ad.1
F|Embassy of the State of Qatar|U|QATAR|o5|d4||a4.1
F|Ministry of Justice of the Republic of Azebraija|U|AZERBAIJAN|6m|1h||9m.1
F|Embassy of the Kingdom of Bahrain to the United|U|BAHRAIN|r3|ck||8a.1
F|Okinawa Prefectural Government of Japan|U|JAPAN|2y|2s||6v.1
F|Embassy of the Republic of Cyprus in the United|U|CYPRUS|r1|d5||6u.1
F|Embassy of the Republic of Serbia|U|SERBIA|qz|dp||6q.1
F|Embassy of Mexico|U|MEXICO|fa|ir||6l.1
F|Turkish Republic of Northern Cyprus (TRNC) Washi|U|CYPRUS|r4|ew||5z.1
F|Ministry of Foreign Affairs of the Arab Republic|U|EGYPT|2u|5y||5q.1
F|Ministry of Foreign Affairs of the Kingdom of Sa|U|SAUDI ARABIA|3q|47||59.1
F|Embassy of Colombia|U|COLOMBIA|1q|9j||4u.1
F|Asociacion Colombiana de Ciudades Capitales|U|COLOMBIA|1p|ah||4u
F|The Government of the Republic of Benin|U|BENIN|45|gj||4s.1
F|Government of the Republic of Angola|U|ANGOLA|3t|g9||4s.1
F|Embassy of the United Arab Emirates|U|UNITED ARAB EMIRATES|9h|2y||4l.1
F|Commissariat of the Holy Land for the USA|U|ISRAEL|px|dg||4j
F|Qatar Foundation for Education, Science and Comm|U|QATAR|bn|hz||47
F|Embassy of India|U|INDIA|ps|gb||3i.1
R|Brownstein Hyatt Farber Schreck, LLP|U|FARA registrant|an|9d||ec
R|Friedlander Consulting Group LLC|U|FARA registrant|9q|39||ck
R|BGR Government Affairs, LLC|U|FARA registrant|mu|bw||ar
R|Vision Americas LLC|U|FARA registrant|9o|5t||ad
R|Kurdistan Regional Government - Liaison Office -|U|FARA registrant|fj|4e||92
R|Akin, Gump, Strauss, Hauer & Feld, LLP|U|FARA registrant|da|8i||82
R|LB International Solutions, LLC|U|FARA registrant|ne|cx||7f
R|Squire Patton Boggs, LLP|U|FARA registrant|bk|co||7b
R|Okinawa Prefecture DC Office, Inc.|U|FARA registrant|74|5b||6v
R|Mercury Public Affairs, LLC|U|FARA registrant|kr|d6||6u
R|Glassman Enterprises, LLC|U|FARA registrant|eb|ga||6k
R|Cornerstone Government Affairs|U|FARA registrant|e5|9p||6c
R|ArentFox Schiff LLP|U|FARA registrant|ih|7w||6c
R|Livingston Group, LLC|U|FARA registrant|j3|bc||59
R|Holland & Knight|U|FARA registrant|ju|ax||52
R|Dentons Global Advisors Government Relations LLC|U|FARA registrant|6h|ad||4y
R|Venable, LLP|U|FARA registrant|d3|ed||4a
A|White House and EOP|U|Executive agency|ck|8t||13t5
A|HHS|U|Executive agency|bi|av||yev
A|Defense|U|Executive agency|97|3y||m8f
A|Treasury|U|Executive agency|fk|8f||k3n
A|Transportation|U|Executive agency|h4|85||heq
A|Commerce|U|Executive agency|mq|88||f9t
A|EPA|U|Executive agency|ep|ae||bsg
A|USDA|U|Executive agency|9m|ex||br8
A|Energy|U|Executive agency|nz|6x||b4n
A|Homeland Security|U|Executive agency|ev|2u||9s1
A|USTR|U|Executive agency|5j|32||83j
A|State|U|Executive agency|m3|3l||7xb
A|Interior|U|Executive agency|mz|fc||7qk
A|Labor|U|Executive agency|6x|7v||5te
A|Education|U|Executive agency|bq|fu||4do
A|Justice|U|Executive agency|p3|dl||3gm
A|SEC|U|Executive agency|ot|gd||27h
A|SBA|U|Executive agency|29|7l||24j
H|Transportation and Infrastructure Committee|U|HSPW|eq|5e||1v
H|Appropriations Committee|U|HSAP|ek|5p||1r
H|Armed Services Committee|U|HSAS|da|4d||1l
H|Energy and Commerce Committee|U|HSIF|fk|97||1i
H|Agriculture Committee|U|HSAG|hg|db||1h
H|Financial Services Committee|U|HSBA|be|6v||1h
H|Foreign Affairs Committee|U|HSFA|c7|56||1h
H|Oversight and Government Reform Committee|U|HSGO|ay|6o||1b
H|Natural Resources Committee|U|HSII|lr|7i||19
H|Ways and Means Committee|U|HSWM|ez|8l||19
H|Judiciary Committee|U|HSJU|jn|ag||18
H|Science, Space, and Technology Committee|U|HSSY|9a|50||14
H|Budget Committee|U|HSBU|et|8o||11
H|Education and Workforce Committee|U|HSED|e6|42||11
H|Homeland Security Committee|U|HSHM|em|64||x
H|Appropriations Committee|U|SSAP|dr|5g||s
H|Senate Committee on Commerce, Science, and Trans|U|SSCM|dc|65||s
H|Intelligence (Permanent Select) Committee|U|HLIG|gc|3a||r
H|Armed Services Committee|U|SSAS|m0|5n||r
H|Senate Committee on Finance|U|SSFI|ma|5c||r
H|Small Business Committee|U|HSSM|hm|3u||q
H|Veterans' Affairs Committee|U|HSVR|aj|51||p
H|Senate Committee on Banking, Housing, and Urban|U|SSBK|kn|35||o
H|House Select Committee on the Strategic Competit|U|HSZS|l6|it||o
H|Senate Committee on Agriculture, Nutrition, and|U|SSAF|dr|4q||n
H|Senate Committee on Health, Education, Labor, an|U|SSHR|62|ez||n
H|Senate Committee on Foreign Relations|U|SSFR|ow|7e||m
H|Senate Committee on the Judiciary|U|SSJU|3y|81||l
H|Senate Select Committee on Intelligence|U|SLIN|g0|9r||l
H|Senate Committee on Energy and Natural Resources|U|SSEG|bi|5w||k
H|Senate Committee on the Budget|U|SSBU|3g|7p||k
H|Joint Economic Committee|U|JSEC|iw|fd||k
H|Senate Committee on Small Business and Entrepren|U|SSSB|d5|eo||j
H|Senate Committee on Veterans' Affairs|U|SSVA|d7|fq||j
H|Senate Committee on Environment and Public Works|U|SSEV|m5|73||i
H|Senate Committee on Rules and Administration|U|SSRA|3c|6n||h
H|Senate Committee on Homeland Security and Govern|U|SSGA|fh|4l||f
H|Rules Committee|U|HSRU|ga|4r||d
H|Senate Special Committee on Aging|U|SPAG|7c|3l||d
H|Committee on House Administration|U|HSHA|a6|5f||c
H|Senate Committee on Indian Affairs|U|SLIA|3n|de||b
H|Joint Committee on Printing|U|JSPR|4a|6q||a
H|Joint Committee on Taxation|U|JSTX|li|6p||a
H|Joint Committee of Congress on the Library|U|JSLC|48|6z||a
H|Commission on Security and Cooperation in Europe|U|JCSE|nf|cn||9
H|United States Senate Caucus on International Nar|U|SCNC|mv|d7||7
H|Senate Select Committee on Ethics|U|SLET|n8|br||6
W|An act to provide for reconciliation pursuant to|R|hr1-119|cz|70||21t.1
W|National Defense Authorization Act for Fiscal Ye|R|hr8800-119|fo|5i||ms
W|National Defense Authorization Act for Fiscal Ye|R|hr2670-118|fc|5v||m8.1
W|National Defense Authorization Act for Fiscal Ye|R|s2296-119|lf|5k||kh
W|National Defense Authorization Act for Fiscal Ye|R|s4784-119|jk|5n||jx
W|Full-Year Continuing Appropriations and Extensio|R|hr1968-119|fw|50||jw.1
W|Servicemember Quality of Life Improvement and Na|R|hr8070-118|g1|5h||is
W|Consolidated Appropriations Act, 2024|R|hr4366-118|lk|9t||hx.1
W|Streamlining Procurement for Effective Execution|R|hr3838-119|f5|67||hm
W|National Defense Authorization Act for Fiscal Ye|D|s2226-118|hz|4x||hi
W|Department of Defense Appropriations Act, 2026|R|hr4016-119|id|52||gu
W|Department of Defense Appropriations Act, 2025|R|hr8774-118|gw|4v||ft
W|Department of Defense Appropriations Act, 2027|R|hr9495-119|9w|b6||fp
W|National Defense Authorization Act for Fiscal Ye|D|s4638-118|i6|4g||fo
W|American Relief Act, 2025|R|hr10545-118|ge|60||ew.1
W|Department of Defense Appropriations Act, 2026|R|s2572-119|cw|4u||eo
W|Department of Defense Appropriations Act, 2024|R|hr4365-118|e4|4g||e0
W|Further Consolidated Appropriations Act, 2024|R|hr2882-118|g9|77||do.1
W|Establishing the congressional budget for the Un|R|hconres14-119|c8|5r||do
W|Department of Defense Appropriations Act, 2025|D|s4921-118|hc|47||cr
W|Tax Relief for American Families and Workers Act|R|hr7024-118|hj|5u||cg
W|Consolidated Appropriations Act, 2026|R|hr7148-119|gk|5j||bw.1
W|Department of Defense Appropriations Act, 2024|D|s2587-118|d9|3s||bv
W|Continuing Appropriations, Agriculture, Legislat|R|hr5371-119|iz|54||b7.1
W|Share the Savings with Seniors Act|R|hr5376-118|gi|cc||b3
W|Departments of Labor, Health and Human Services|R|hr9260-119|gj|46||an
W|Departments of Labor, Health and Human Services|R|s2587-119|is|61||ad
W|BUILD America 250 Act|R|hr8870-119|hr|49||a9
W|Departments of Labor, Health and Human Services|R|hr9029-118|en|4r||a6
W|Transportation, Housing and Urban Development, a|R|hr9028-118|iq|5s||a2
U|Congressional Equality Caucus|U|Caucus|5e|9e||4h
U|Republican Study Committee|U|Caucus|i4|dx||4a
U|Congressional Taiwan Caucus|U|Caucus|in|d0||3k
U|Congressional Black Caucus|U|Caucus|5w|7k||2n
U|Congressional Western Caucus|U|Caucus|h2|cs||2e
U|Congressional Asian Pacific American Caucus|U|Caucus|6d|c0||2c
U|Congressional Progressive Caucus|U|Caucus|68|9k||25
U|Climate Solutions Caucus|U|Caucus|di|df||1q
B|American Israel Public Affairs Committee|U|Form 3L bundler|86|c5||gix
B|J Street|U|Form 3L bundler|4k|fy||16l
B|Mortgage Bankers Association|U|Form 3L bundler|4o|8a||1q
B|League Of Conservation Voters|U|Form 3L bundler|44|il||10
B|National Association Of Broadcasters|U|Form 3L bundler|by|ec||x
M|Nicholas A. Langworthy|R|H-NY-23|||bk|37.2u4.9v.y.4u.0.3.0.0.7v.0.7.76.l.0.0.3.2.0.0.7t
M|Lucy McBath|D|H-GA-6|||bj|au.pj.3l.0.29.7k.0.5.2.1p.9.3.3n.l.1b.0.2.4.5.0.7u
M|Betty McCollum|D|H-MN-4|||bj|3s.2mt.99.0.36.f.0.5.2.r.8.5.ar.8.0.0.1.0.1k.0.7v
M|Barry Moore|R|H-AL-1|||bi|98.xe.5l.19.1o.d78.17c.1.2.1c.a.0.55.q.0.0.2.3.9.0.7w
M|Warren Davidson|R|H-OH-8|||bi|a3.s8.52.q.1t.3.0.5.2.3u.k.6.2n.9.2.0.2.4.0.0.7x
M|Josh Harder|D|H-CA-9|||bh|84.192.3h.0.2i.2b.12a.1.5.2k.7.1.26.2.2.0.1.2.0.0.7z
M|Brian Jack|R|H-GA-3|||be|2g.30q.8u.jy.6a.23y.1s.0.1.9.3.d.li.4.0.0.3.0.0.0.80
M|Scott Perry|R|H-PA-10|||be|ak.bb.3y.fr.s.2u4.a13.0.2.1m.k.8.z.h.0.0.4.3.0.0.81
M|Ron Estes|R|H-KS-4|||bb|66.1k1.cw.0.31.0.0.0.1.6p.f.4.41.h.0.0.3.2.f.0.83
M|Ami Bera|D|H-CA-6|||ba|7z.16x.6n.0.2l.n.0.0.7.13.y.b.84.u.1.0.2.5.r.0.84
M|Robert P. Bresnahan, Jr.|R|H-PA-8|||b9|7h.pr.93.iw.22.1ed.e23.1.0.11.5.1.i.4.1u.2n.3.1.4.0.85
M|Madeleine Dean|D|H-PA-4|||b7|95.wy.7m.0.26.0.0.6.4.28.c.i.25.g.0.0.2.2.1y.0.86
M|Lauren Underwood|D|H-IL-14|||b7|93.12l.22.1.34.4h.0.3.3.4q.9.4.6u.5.0.0.1.3.0.0.87
M|Gabe Vasquez|D|H-NM-2|||b7|5j.1tn.9w.0.5z.pm.3gl.0.0.1b.a.7.20.2.0.0.2.2.6.0.88
M|Hillary J. Scholten|D|H-MI-3|||b7|7l.18a.89.4.4v.be.hv.1.1.38.7.3.3u.9.0.0.2.1.3.0.89
M|Janice D. Schakowsky|D|H-IL-9|||b6|bh.lw.2s.0.1q.0.0.9.5.56.c.2.1t.m.0.0.1.4.0.0.8a
M|Jason Crow|D|H-CO-6|||b6|9e.109.1e.16.1o.b.0.3.5.28.i.d.42.k.0.0.2.1.t.0.8b
M|Aaron Bean|R|H-FL-4|||b6|3f.2n7.dm.5.6a.0.0.1.0.26.9.3.5y.d.2.0.1.2.a.0.8c
M|Scott Franklin|R|H-FL-18|||b5|83.17w.4s.0.2b.0.0.6.1.1c.a.3.6h.p.i.2f.2.2.1t.0.8d
M|Nicholas J. Begich III|R|H-AK-0|||b5|9d.q5.81.4o.1x.2zs.dui.1.2.2l.0.4.k.2.5.0.3.2.4.0.8e
M|James P. McGovern|D|H-MA-2|||b3|79.1he.2n.0.2j.0.0.4.2.2p.d.6.30.a.0.0.2.2.0.0.8g
M|Jamie Raskin|D|H-MD-8|||b3|9q.v1.4f.n.2u.4.0.5.8.1y.d.5.3u.b.2.0.1.4.0.0.8h
M|Kristen McDonald Rivet|D|H-MI-8|||b3|5k.1v6.7t.b.6k.14c.15p.0.2.1u.3.1.1m.a.0.0.2.1.0.0.8i
M|Sean Casten|D|H-IL-6|||b2|ag.oq.6j.0.1l.25.0.5.7.3k.7.2.a.w.0.0.2.1.0.0.8k
M|Tina Smith|D|S-MN|||ax|8s.14c.24.0.1j.0.0.4.2.5i.6.c.i.0.5.8.4.0.0.0.8m
M|Emilia Strong Sykes|D|H-OH-13|||ax|6r.1eb.a2.3.58.1wi.1g2.1.2.1o.3.1.3f.a.0.0.2.3.0.0.8n
M|Salud O. Carbajal|D|H-CA-24|||aw|af.p1.6r.0.1j.15.0.1.7.2v.f.6.3j.x.0.0.3.7.v.0.8o
M|James A. Himes|D|H-CT-4|||au|8x.uu.ak.0.2b.0.0.7.6.f.e.8.23.u.2.1.2.4.14.0.8p
M|Derrick Van Orden|R|H-WI-3|||at|9c.m9.9y.75.1m.20l.f9j.0.2.2o.7.3.32.6.0.0.3.0.i.0.8q
M|Grace Meng|D|H-NY-6|||at|av.ox.46.0.1w.0.0.6.5.1s.g.9.1t.h.5.0.1.4.0.0.8r
M|Ryan Mackenzie|R|H-PA-7|||at|7n.rv.6p.i2.24.102.ezl.0.0.1b.d.0.1o.5.0.0.3.0.0.0.8s
M|Jared F. Golden|D|H-ME-2|||ar|9t.ux.4d.d.2l.130.4yh.0.2.1x.c.8.50.6.0.0.2.1.0.0.8t
M|Lois Frankel|D|H-FL-22|||aq|cu.bt.3g.0.14.5e.2y.4.2.11.o.7.1g.f.1x.3y.1.4.2.0.8u
`;
const RSD = `
M|John B. Larson|D|H-CT-1|||an|78.1be.8v.0.2x.1e.45.3.6.z.9.2.4r.4.1.0.1.4.5.0.8v
M|Robert Garcia|D|H-CA-42|||ae|5q.1vs.4y.q.4t.8l.0.0.0.1b.a.0.6e.k.1.0.2.2.0.0.8w
M|Randy K. Weber, Sr.|R|H-TX-14|||ae|an.ok.5p.0.1m.2.0.1.8.45.c.4.3a.v.0.0.2.3.e.0.8x
M|Andrea Salinas|D|H-OR-6|||ad|4g.2ce.93.0.7b.v.q.0.2.27.4.2.6m.i.0.0.2.3.6.0.8y
M|Mike Quigley|D|H-IL-5|||ac|a8.sa.53.0.1x.0.0.8.8.17.g.7.1t.i.0.0.2.1.9.0.8z
M|Suzanne Bonamici|D|H-OR-1|||ab|ad.s9.3l.0.1f.b.0.8.3.56.3.5.1e.2.2.0.2.4.0.0.90
M|Christopher H. Smith|R|H-NJ-4|||aa|d2.co.1g.6.10.3n.0.6.4.2p.w.0.6m.2.0.0.1.3.0.0.91
M|Brittany Pettersen|D|H-CO-7|||a9|6c.1ie.af.0.5t.2s.0.1.2.2b.5.3.2o.a.1.0.1.1.0.0.92
M|Chip Roy|R|H-TX-21|||a9|9l.x1.1v.2k.1r.c.0.1.5.47.8.3.8d.g.2.1.3.1.0.0.93
M|Michelle Fischbach|R|H-MN-7|||a8|7k.15l.ai.n.2w.4m.0.1.2.29.5.5.2k.k.0.0.2.2.l.0.94
M|Paul Tonko|D|H-NY-20|||a7|ah.mp.8h.0.25.0.0.6.3.3n.9.3.23.m.0.0.2.3.0.0.95
M|Jake Auchincloss|D|H-MA-4|||a7|9j.u4.73.j.2k.5o.0.1.3.24.a.5.1j.k.0.0.1.2.1.0.96
M|Eric A. "Rick" Crawford|R|H-AR-1|||a7|75.1di.89.0.2k.0.0.2.2.2z.d.3.4g.7.0.0.3.2.j.0.97
M|Brian Babin|R|H-TX-36|||a6|8w.vq.7p.29.2a.d.0.1.4.2j.7.6.2q.e.7.2.2.4.1f.0.98
M|Daniel S. Goldman|D|H-NY-10|||a4|aj.s6.23.s.2h.7z.31.0.2.20.d.1.6m.8.5d.a5.2.3.0.0.99
M|Richard McCormick|R|H-GA-7|||a4|a0.v4.3e.4.20.67.0.0.1.1h.k.e.2n.j.6.d.3.2.t.0.9a
M|Craig A. Goldman|R|H-TX-12|||a4|71.1bu.7h.2p.3f.11k.18.0.1.23.6.0.s.b.0.0.1.0.j.0.9b
M|Elizabeth Warren|D|S-MA|||a3|ex.h.0.0.5.0.bc.5.8.6a.8.b.x.0.0.0.4.0.0.0.9c
M|Julie Johnson|D|H-TX-32|||a3|8t.14a.1w.0.34.1ub.4m.0.0.1c.9.0.48.7.4c.23.4.0.9.0.9d
M|Jake Ellzey|R|H-TX-6|||a3|3w.2e0.c7.4n.4d.3r.0.0.0.3.d.3.9z.f.0.0.2.2.10.0.9e
M|Julie Fedorchak|R|H-ND-0|||a1|7a.17m.ak.16.37.8g.g6.0.2.1x.5.3.k.a.0.0.1.2.0.0.9g
M|Gary J. Palmer|R|H-AL-6|||a0|at.mw.68.0.1q.3n.0.0.2.3g.e.6.2g.k.2.0.2.2.l.0.9h
M|Christopher R. Deluzio|D|H-PA-17|||a0|9v.uf.4z.4.2h.87.1g.0.2.5c.7.8.4r.7.0.0.2.1.0.0.9i
M|Jasmine Crockett|D|H-TX-30|||9z|ar.pb.4i.0.2o.rw.3gc.2.3.16.a.5.u.6.0.0.3.2.0.0.9j
M|Peter Welch|D|S-VT|||9z|be.op.d.0.1l.0.0.4.5.8a.b.5.20.0.1.0.4.2.a.0.9k
M|Shomari Figures|D|H-AL-2|||9z|6y.1fr.6t.5.4j.5bf.2j4.1.1.v.3.4.30.3.0.0.2.1.0.0.9l
M|Derek Tran|D|H-CA-45|||9x|7r.18c.6s.9.41.3wm.bo.0.2.h.6.5.50.4.6.0.2.2.0.0.9n
M|Judy Chu|D|H-CA-28|||9x|b4.na.32.0.1b.0.0.4.6.3v.b.6.19.4.2.0.2.4.3.0.9o
M|Sam T. Liccardo|D|H-CA-16|||9x|7m.1ai.5l.j.3r.1fa.9v.0.0.1c.7.1.3h.9.4.0.1.3.0.0.9p
M|Sharice Davids|D|H-KS-3|||9w|64.1oe.8z.0.5s.5r.0.1.1.1m.6.4.1j.8.0.0.2.0.4.0.9q
M|Dale W. Strong|R|H-AL-5|||9u|4f.2dp.8k.8.4r.0.0.2.0.13.d.5.6a.5.0.0.2.1.8.0.9r
M|Nanette Diaz Barragán|D|H-CA-44|||9s|69.1m4.9m.0.3g.0.0.2.6.22.4.5.8u.9.0.0.1.5.z.0.9s
M|Eugene Simon Vindman|D|H-VA-7|||9s|8g.15e.42.4.4e.1wv.1e2.0.0.1r.9.2.7k.7.0.0.2.1.0.0.9t
M|Val T. Hoyle|D|H-OR-4|||9r|7g.1bz.61.0.2t.8m.oq.0.1.1n.0.8.c.0.w.1e.2.1.0.0.9u
M|Maxine Waters|D|H-CA-43|||9n|a4.tx.40.0.1q.0.0.5.4.2f.9.4.2g.g.0.0.1.4.0.0.9x
M|Pat Harrigan|R|H-NC-10|||9j|8b.15n.4f.b.2n.oa.8.0.0.1h.9.3.2i.d.1.0.2.0.0.0.9y
M|Jeff Hurd|R|H-CO-3|||9g|80.15s.6l.z.3a.1z4.21g.0.0.12.6.2.2l.i.0.0.3.2.d.0.a0
M|Tom Barrett|R|H-MI-7|||9g|9a.od.91.6f.22.29x.lgg.1.0.1i.5.1.k.4.0.0.2.0.0.0.a1
M|Marc A. Veasey|D|H-TX-33|||9g|88.10u.ag.0.2k.0.0.3.3.i.l.c.8e.h.0.0.1.5.8.0.a2
M|Kevin Kiley|I|H-CA-3|||9e|b1.l6.5l.15.1k.1tn.2lv.0.0.3w.7.2.1j.8.0.0.3.4.0.0.a4
M|Brad Knott|R|H-NC-13|||9b|5u.1rd.8m.j.4r.5l.a5.1.0.f.8.1.2g.8.0.0.4.0.0.0.a6
M|Ron Johnson|R|S-WI|||9a|eg.41.k.0.c.2e.0.b.4.2a.f.6.s.0.1.0.4.0.0.0.a7
M|Cory Mills|R|H-FL-7|||9a|9u.y6.1c.4.1r.0.b6.0.0.m.t.c.5u.w.0.0.2.1.0.0.a8
M|Laura Gillen|D|H-NY-4|||9a|9n.x1.3k.1.3l.3zw.1pv.0.0.3t.3.1.2g.2.0.0.2.1.9.0.a9
M|Randy Fine|R|H-FL-6|||96|9f.xz.1y.2t.25.2v0.26.0.0.1q.7.0.92.5.4.0.2.0.6.0.aa
M|Pat Fallon|R|H-TX-4|||94|cp.dq.2m.0.14.0.0.3.2.2e.n.7.0.a.b.0.3.4.9.0.ab
M|Michael Baumgartner|R|H-WA-5|||94|bl.kc.3i.0.1f.3k.ic.0.1.3u.d.1.a.8.0.0.3.1.8.0.ac
M|Lance Gooden|R|H-TX-5|||94|b6.jp.46.2c.1c.0.0.0.2.47.k.5.4g.e.3.0.2.2.0.0.ad
M|Dave Min|D|H-CA-47|||8z|8p.14i.2q.0.2m.2q7.68f.0.0.q.5.0.4e.6.3.0.3.2.0.0.ae
M|John Garamendi|D|H-CA-8|||8y|by.h2.3b.0.1b.0.0.3.4.2f.m.8.2g.7.1.0.2.2.b.0.af
M|Ro Khanna|D|H-CA-17|||8v|dm.ag.1.0.g.31.12.1.4.2g.j.a.14.h.0.0.3.5.5.0.ah
M|Clay Higgins|R|H-LA-3|||8u|d1.9a.15.3w.a.0.0.5.2.3h.f.2.0.j.0.0.3.2.0.0.ai
M|Sarah McBride|D|H-DE-0|||8t|7s.1bb.3u.0.3f.c1.0.0.0.t.a.3.6y.e.0.0.2.0.0.0.aj
M|Chuck Edwards|R|H-NC-11|||8r|b2.n4.4k.5.21.i.o2.1.1.1m.6.3.2u.m.1.0.2.2.d.0.ak
M|Troy E. Nehls|R|H-TX-22|||8r|am.qo.3s.0.21.1g.0.3.3.3h.8.0.24.6.0.0.3.2.g.0.al
M|Jeff Crank|R|H-CO-5|||8n|7y.185.54.r.3o.1l0.1xy.0.1.c.8.2.1m.6.0.0.2.1.0.0.an
M|Wesley Bell|D|H-MO-1|||8n|9g.z7.3d.0.3b.4lp.jj.0.2.n.5.4.1c.b.0.0.3.3.0.0.ao
M|Pramila Jayapal|D|H-WA-7|||8m|eb.5i.h.0.o.1.0.6.6.3n.a.7.0.d.1.1.3.2.0.0.ap
M|John J. McGuire III|R|H-VA-5|||8m|aq.px.1a.2p.21.25k.2nh.0.0.u.8.3.3s.8.6.3.2.0.0.0.ar
M|Ed Case|D|H-HI-1|||8l|89.15b.5z.0.26.0.0.0.1.14.h.a.60.e.5.0.1.4.p.0.at
M|Maggie Goodlander|D|H-NH-2|||8l|7x.15s.2m.5o.36.tm.2v.1.0.8.8.4.6d.6.0.0.3.0.0.0.au
M|Bernard Sanders|I|S-VT|||8k|ey.c.1.0.6.0.0.9.e.dl.7.3.0.0.0.0.5.1.0.0.av
M|Michael F. Bennet|D|S-CO|||8k|e4.5e.e.18.e.0.0.a.6.6z.8.3.1m.0.0.0.4.1.4.0.aw
M|Bennie G. Thompson|D|H-MS-2|||8j|8a.116.9l.0.2f.0.0.5.2.s.6.0.7q.f.2.0.1.4.0.0.ax
M|Sarah Elfreth|D|H-MD-3|||8i|81.1aa.2t.0.3q.3e5.0.0.0.j.6.5.37.6.0.0.2.1.4.0.ay
M|Jared Huffman|D|H-CA-2|||8i|b7.ne.2q.0.1d.0.0.4.1.3u.5.5.1n.i.1.0.2.2.0.0.az
M|George Whitesides|D|H-CA-27|||8h|as.ny.54.6.1o.39j.1vn.1.0.19.3.4.y.2.7.7.2.1.0.0.b0
M|Michael Guest|R|H-MS-3|||8e|7p.1c1.4f.0.2l.0.0.1.3.b.5.6.5z.l.r.10.3.2.2.0.b1
M|Thomas Massie|R|H-KY-4|||8e|cx.d4.1q.0.y.31z.82l.0.5.1q.5.3.f.1.1.0.2.1.0.0.b2
M|Jennifer L. McClellan|D|H-VA-4|||8c|9p.u1.65.0.2f.u.0.1.0.1p.7.8.4m.u.1.2.1.2.0.0.b3
M|Wesley Hunt|R|H-TX-38|||8c|bx.fk.29.2k.17.pz.a24.0.1.10.8.3.u.8.2.0.2.0.0.0.b4
M|Josh Riley|D|H-NY-19|||8c|92.10z.3r.1.3k.48e.2hp.0.2.n.4.4.5q.3.0.0.2.1.0.0.b5
M|Riley M. Moore|R|H-WV-2|||8b|9i.wg.4q.x.2h.xc.0.0.1.y.a.0.a.3.2.0.1.0.7.0.b6
M|Joe Courtney|D|H-CT-2|||84|bs.hw.46.0.1n.0.0.3.4.2b.d.4.k.8.0.0.2.1.m.0.b7
M|Joe Wilson|R|H-SC-2|||83|c5.fm.3h.0.14.0.0.3.3.1a.1a.0.9o.d.0.0.3.2.2h.0.b8
M|Mark Takano|D|H-CA-39|||81|d4.bf.2j.0.19.3x.0.1.4.24.b.1.3a.g.1.0.2.4.1i.0.b9
M|Michael A. Rulli|R|H-OH-6|||80|87.13p.6y.o.3g.12.40.0.0.1a.2.0.1o.8.k.7.2.1.0.0.ba
M|Glenn Grothman|R|H-WI-6|||80|cj.e1.32.0.14.4.b.5.1.3i.6.2.1q.8.1.0.4.4.0.0.bb
M|Nydia M. Velázquez|D|H-NY-7|||7y|dl.9t.r.0.u.0.0.8.5.2l.8.5.k.7.0.0.2.5.0.0.bc
M|Mary Gay Scanlon|D|H-PA-5|||7y|cn.bx.4v.0.14.1.0.1.6.3z.7.3.1l.9.4.2.2.2.0.0.bd
M|Julia Brownley|D|H-CA-26|||7x|cq.df.2w.0.q.6q.0.1.5.31.5.3.a.6.1.0.3.1.0.0.be
M|Elijah Crane|R|H-AZ-2|||7x|e6.46.h.1u.7.39t.2ko.0.4.x.a.2.0.j.0.0.2.1.0.0.bf
M|Jefferson Van Drew|R|H-NJ-2|||7w|di.8s.27.6.p.di.159.1.4.2t.2.b.21.1.0.0.2.2.0.0.bh
M|Lizzie Fletcher|D|H-TX-7|||7w|9m.rc.8g.15.29.o.0.0.2.19.a.f.1c.d.0.0.1.1.0.0.bi
M|Mike Haridopolos|R|H-FL-8|||7w|72.1ds.50.38.2g.q2.0.0.0.6.6.3.ci.5.0.0.2.0.4.0.bj
M|Jonathan L. Jackson|D|H-IL-1|||7v|cf.g7.1o.0.1h.46.0.0.3.6.j.0.2s.f.w.1z.2.1.7.0.bk
M|James R. Walkinshaw|D|H-VA-11|||7u|6z.1ip.3v.0.3y.s5.3.0.0.k.2.5.3a.4.0.0.2.3.0.0.bl
M|Andrew Ogles|R|H-TN-5|||7u|do.81.1w.0.p.ni.0.0.1.2f.a.2.f.q.0.0.2.4.b.0.bm
M|Shri Thanedar|D|H-MI-13|||7r|ed.4b.r.0.l.272.cv.2.1.w.9.4.5.2.g.o.2.3.0.0.bn
M|J. Luis Correa|D|H-CA-46|||7q|ay.iq.9t.1.1l.2z.0.1.5.17.2.g.p.a.0.0.2.4.a.0.bo
M|Robert F. Onder, Jr.|R|H-MO-3|||7p|dv.5u.2f.0.o.1b4.1wl.0.2.2d.4.1.f.7.6.0.3.1.5.0.bp
M|Mark B. Messmer|R|H-IN-8|||7n|9w.on.4g.6c.1u.1hr.26.0.0.z.7.5.a.6.0.0.3.2.0.0.bq
M|Andrew S. Clyde|R|H-GA-9|||7n|de.bf.t.0.b.10.18.2.3.23.8.3.19.n.1.0.2.1.h.0.br
M|Gwen Moore|D|H-WI-4|||7n|86.158.6c.0.2n.s.0.1.2.1i.8.0.14.3.0.0.2.4.a.0.bs
M|Tim Moore|R|H-NC-14|||7n|ap.lc.4l.41.1h.m5.0.1.0.n.7.0.w.4.l.a.2.1.c.0.bt
M|Mike Ezell|R|H-MS-4|||7m|85.16u.5m.1.2u.24.0.0.0.25.8.3.2u.2.0.0.2.1.5.0.bu
M|Sylvia R. Garcia|D|H-TX-29|||7k|c8.dm.55.0.w.fi.0.1.2.1y.8.0.3b.7.0.0.2.3.0.0.bv
M|William R. Keating|D|H-MA-9|||7k|bm.m4.1g.0.1b.0.0.2.2.o.n.c.3t.1.p.g.2.2.1.0.bw
M|Bonnie Watson Coleman|D|H-NJ-12|||7g|ce.fe.2i.0.y.0.0.3.8.2a.4.9.1b.9.0.0.2.6.0.0.bx
M|Stephen F. Lynch|D|H-MA-8|||7f|dt.6m.22.0.v.26.5y.5.3.l.8.3.1l.6.3.0.2.3.0.0.bz
M|Victoria Spartz|R|H-IN-5|||7c|e8.5s.i.0.8.87.357.3.6.g.6.4.z.5.0.0.1.1.n.0.c1
M|Summer L. Lee|D|H-PA-12|||7b|dw.7m.h.0.h.lz.0.1.1.49.4.0.0.8.0.0.2.2.0.0.c2
M|Anna Paulina Luna|R|H-FL-13|||7a|e0.3w.n.2z.a.o9.4pj.0.2.x.b.3.0.c.0.0.2.3.7.0.c3
M|Frank J. Mrvan|D|H-IN-1|||79|6x.1a4.cn.0.3x.4u.0.0.2.9.6.3.37.1.0.0.1.1.0.0.c4
M|André Carson|D|H-IN-7|||78|bd.ja.61.0.14.0.0.2.6.o.b.4.0.l.0.0.3.5.0.0.c5
M|Deborah K. Ross|D|H-NC-2|||77|c4.ba.80.0.s.1.0.1.4.1x.7.4.k.9.d.5.3.2.0.0.c6
M|Paul A. Gosar|R|H-AZ-9|||77|ee.4s.5.0.9.0.0.5.6.2d.9.2.a.f.0.0.2.5.7.0.c7
M|James C. Justice|R|S-WV|||72|ax.lm.55.1u.1p.2wg.1mi.0.0.1h.3.3.3m.0.0.0.4.0.0.0.c8
M|Ilhan Omar|D|H-MN-5|||71|ej.32.c.0.d.kp.1v.1.3.r.b.a.q.b.0.0.2.4.a.0.c9
M|Norma J. Torres|D|H-CA-35|||70|c0.h3.2v.0.1l.0.0.4.3.1m.a.0.28.7.1.0.2.3.1j.0.ca
M|Emily Randall|D|H-WA-6|||70|bq.l4.1x.0.1n.22i.0.1.0.q.4.2.1k.b.1.1.2.1.1.0.cb
M|Jahana Hayes|D|H-CT-5|||6y|cd.dt.4d.0.29.cp.3q.1.2.1s.5.3.2e.4.0.0.2.4.0.0.cc
M|Nancy Pelosi|D|H-CA-11|||6x|dk.79.j.2s.n.0.0.h.a.1.8.3.28.0.l.w.0.3.25.0.ce
M|Suhas Subramanyam|D|H-VA-10|||6w|aa.up.21.0.38.ne.0.0.0.14.5.1.15.a.0.0.3.2.2.0.cf
M|Troy Downing|R|H-MT-2|||6w|bp.ij.4c.7.1e.ob.0.0.1.1o.5.1.p.c.0.0.2.1.0.0.cg
M|Timothy M. Kennedy|D|H-NY-26|||6v|9o.wf.3v.2.2j.1x.0.1.0.1f.9.1.23.3.1.0.2.2.5.0.ch
M|John W. Rose|R|H-TN-6|||6v|el.25.p.0.7.0.0.4.5.1y.9.2.1.9.4.0.2.2.0.0.ci
M|Morgan McGarvey|D|H-KY-3|||6u|8o.11b.60.0.2i.3.0.0.1.1l.3.3.1w.e.3.6.3.1.1i.0.cj
M|Joaquin Castro|D|H-TX-20|||6u|bo.m4.11.0.1h.0.0.1.3.10.o.g.51.6.0.0.2.3.c.0.ck
M|Henry C. "Hank" Johnson, Jr.|D|H-GA-4|||6u|co.c7.47.0.1d.0.0.1.6.1u.b.0.1q.h.0.0.2.6.9.0.cl
M|Alma S. Adams|D|H-NC-12|||6r|df.96.2n.0.j.0.0.6.a.1g.8.3.15.5.0.0.2.4.0.0.cm
M|John Fetterman|D|S-PA|||6q|dq.8f.d.r.o.1m.0.2.0.2z.5.7.w.0.c.8.4.0.0.0.cn
M|Maxine Dexter|D|H-OR-3|||6q|ae.u4.1p.0.1p.1ph.2.0.0.q.4.1.b.9.0.0.2.0.0.0.co
M|Morgan Luttrell|R|H-TX-8|||6p|bb.jn.2a.3l.1f.7.0.1.1.s.d.8.5.h.0.0.3.1.0.0.cp
M|Tracey Mann|R|H-KS-1|||6n|a1.r3.73.d.1n.0.0.0.1.2y.7.4.p.b.0.0.2.2.0.0.cq
M|Lauren Boebert|R|H-CO-4|||6n|cw.e1.r.8.o.mz.1fc.0.3.1m.4.3.k.1.0.0.2.6.0.0.cr
M|Jill N. Tokuda|D|H-HI-2|||6k|c2.ii.12.0.18.0.0.0.2.1p.e.7.z.k.0.0.3.3.16.0.cs
M|Johnny Olszewski, Jr.|D|H-MD-2|||6h|br.jz.2c.0.1m.5w.0.1.0.j.a.3.z.b.1.0.2.1.3.0.ct
M|Sara Jacobs|D|H-CA-51|||6h|ds.8a.g.1.u.0.0.0.0.1x.s.6.12.k.2.0.2.3.9.0.cu
M|Mark Pocan|D|H-WI-2|||6c|d6.bx.1e.0.16.0.0.5.4.10.a.2.l.9.0.0.2.3.0.0.cv
M|Brandon Gill|R|H-TX-26|||6b|bu.hy.2x.k.1i.pq.r0.0.1.15.3.0.14.a.0.0.3.0.0.0.cw
M|Tony Wied|R|H-WI-8|||6b|bc.kr.4i.6.1a.4.ja.1.0.p.4.0.p.2.4.0.3.1.0.0.cx
M|Seth Magaziner|D|H-RI-2|||68|b8.lc.4r.0.1y.1.0.1.1.22.8.2.16.3.2.1.2.1.0.0.cz
M|Valerie P. Foushee|D|H-NC-4|||67|dc.98.3a.0.t.1u8.6q.0.0.1j.5.3.z.a.0.0.2.3.5.0.d0
M|Jerrold Nadler|D|H-NY-12|||63|ca.f6.3b.0.z.0.0.2.8.1f.4.8.1j.5.0.0.2.3.0.0.d1
M|Shontel M. Brown|D|H-OH-11|||62|8u.zs.6c.0.2b.4.0.1.1.z.6.2.16.5.0.0.3.2.0.0.d2
M|Sydney Kamlager-Dove|D|H-CA-37|||62|ai.qb.4t.0.2j.0.0.1.0.1v.3.4.n.q.0.0.2.3.f.0.d3
M|Stacey E. Plaskett|D|H-VI-0|||61|9s.wz.2y.0.1o.0.0.1.3.s.6.6.2m.8.0.0.3.4.1g.0.d4
M|Keith Self|R|H-TX-3|||61|d8.cj.k.0.z.0.0.0.1.1f.o.c.12.o.0.0.3.1.1a.0.d5
M|Nellie Pou|D|H-NJ-9|||60|8j.13w.57.0.4h.2k.4c.0.0.g.5.2.5f.1.0.0.2.2.1.0.d6
M|April McClain Delaney|D|H-MD-6|||5z|bk.kw.2w.4.1e.f9.6g.0.0.v.1.1.u.2.8.l.2.2.0.0.d7
M|Addison P. McDowell|R|H-NC-6|||5y|8h.13s.4w.r.28.5h.0.0.0.f.4.0.46.6.0.0.3.0.0.0.d8
M|Cleo Fields|D|H-LA-6|||5y|cm.gg.e.0.p.8c.0.2.1.6.4.1.1j.5.a.1a.1.1.0.0.d9
M|Al Green|D|H-TX-9|||5x|ek.30.8.0.6.0.1b.5.3.r.d.2.0.1.0.0.2.4.0.0.db
M|Melanie A. Stansbury|D|H-NM-1|||5x|ck.ft.18.0.1o.1f.0.1.5.1c.5.3.2.8.0.0.2.2.8.0.dc
M|John W. Mannion|D|H-NY-22|||5w|bf.l6.3q.4.1y.2hz.12x.0.1.g.4.1.1r.0.0.0.2.1.0.0.dd
M|Jefferson Shreve|R|H-IN-6|||5w|dh.7m.3k.4.n.2j.0.0.0.v.9.1.a.n.y.1r.1.0.f.0.de
M|Sheri Biggs|R|H-SC-3|||5s|cs.b7.2z.1j.11.a0.0.0.1.u.9.0.2a.4.5.3.3.0.5.0.dg
M|Veronica Escobar|D|H-TX-16|||5p|ab.sw.3o.0.25.0.0.0.1.y.b.9.30.7.0.0.2.3.6.0.dh
M|Derek Schmidt|R|H-KS-2|||5p|aw.o1.4t.0.1s.99.24.0.0.d.7.3.0.7.0.0.3.0.0.0.di
M|Juan Vargas|D|H-CA-52|||5p|dg.9a.2k.0.l.0.0.4.2.n.e.3.1u.7.0.0.1.5.1.0.dj
M|Maxwell Frost|D|H-FL-10|||5o|bw.je.15.0.22.d.0.0.3.1h.5.2.3r.k.0.0.2.3.0.0.dk
M|Delia C. Ramirez|D|H-IL-3|||5o|bv.ju.14.9.r.0.0.1.1.1l.7.2.0.p.0.0.2.2.7.0.dl
M|Dwight Evans|D|H-PA-3|||5n|cz.cd.28.0.t.j.0.1.2.q.8.4.a.2.m.g.1.3.0.0.dm
M|Eric Burlison|R|H-MO-7|||5m|c6.f6.3m.7.1h.c.0.0.1.2e.4.1.1e.q.0.0.2.1.0.0.dn
M|Mark DeSaulnier|D|H-CA-10|||5l|ch.gl.q.0.l.0.0.5.2.1c.5.2.0.0.1.0.3.3.b.0.dp
M|Becca Balint|D|H-VT-0|||5l|bj.lt.24.0.1r.4d.0.0.3.z.6.2.1o.3.0.0.2.0.6.0.dq
M|Daniel Webster|R|H-FL-11|||5k|cb.fa.2y.a.18.d.0.2.3.i.6.2.u.l.0.0.3.1.0.0.dr
M|Tim Burchett|R|H-TN-2|||5j|eh.1y.1e.k.5.0.0.1.1.1n.n.8.19.a.0.0.3.1.0.0.ds
M|Teresa Leger Fernandez|D|H-NM-3|||5i|c1.gi.38.0.18.p.0.0.0.2c.4.2.12.c.1.0.2.3.e.0.dt
M|Tom McClintock|R|H-CA-5|||5h|dx.6q.14.0.x.0.0.4.4.1s.6.3.u.5.0.0.3.4.0.0.du
M|Alexandria Ocasio-Cortez|D|H-NY-14|||5g|eu.p.1.0.c.2.fe.1.2.22.1.1.1.6.0.0.1.3.0.0.dv
M|Matt Van Epps|R|H-TN-7|||5f|bz.gq.3g.0.18.1uk.19m.0.0.k.0.0.1c.0.1.1.2.1.0.0.dw
M|Yassamin Ansari|D|H-AZ-3|||5d|d5.ci.w.0.12.206.39.0.0.1c.2.5.f.1.0.0.2.2.1.0.dx
M|Kevin Mullin|D|H-CA-15|||5d|b0.n9.4p.0.29.0.0.0.3.11.7.3.19.e.0.0.1.4.0.0.dy
M|Chellie Pingree|D|H-ME-1|||58|e9.4a.1q.0.d.0.0.1.1.2w.9.2.5.d.0.0.2.1.0.0.e0
M|Mary E. Miller|R|H-IL-15|||55|ec.4b.u.0.c.l.2.2.0.1x.5.0.u.m.0.0.4.1.5.0.e1
M|Adelita S. Grijalva|D|H-AZ-7|||52|bi.nk.m.0.1d.if.5g.0.0.m.1.0.f.4.0.0.2.2.0.0.e2
M|George Latimer|D|H-NY-16|||50|e2.6a.12.0.10.4be.vt.0.0.9.7.1.u.6.0.0.2.2.0.0.e3
M|Barry Loudermilk|R|H-GA-11|||4z|du.5k.31.2.j.0.0.2.6.1i.6.3.w.6.0.0.3.4.5.0.e4
M|Burgess Owens|R|H-UT-4|||4x|ci.ep.1s.m.11.0.0.0.1.3h.3.1.14.g.0.0.2.2.5.0.e5
M|Eleanor Holmes Norton|D|H-DC-0|||4v|ew.2.e.0.1.0.0.0.8.2r.3.2.0.3.2.0.2.7.0.0.e6
M|Scott DesJarlais|R|H-TN-4|||4p|cr.dk.2i.0.l.0.0.1.4.1.b.8.0.1.1.1.2.3.3.0.e7
M|Christian D. Menefee|D|H-TX-18|||4m|d3.do.d.0.w.5im.0.0.0.4.0.0.2.0.0.0.2.1.0.0.e8
M|Jesús G. "Chuy" García|D|H-IL-4|||4j|cv.e4.11.0.w.0.0.1.4.12.6.0.k.c.0.0.2.4.0.0.e9
M|Rashida Tlaib|D|H-MI-12|||4h|es.16.2.0.8.5.m.1.2.1i.a.3.0.2.0.0.2.2.0.0.ea
M|Mark Harris|R|H-NC-8|||4h|e7.5a.11.0.h.d.4t.0.0.n.6.0.5.9.j.0.3.1.0.0.eb
M|Kweisi Mfume|D|H-MD-7|||46|da.b4.1l.0.16.0.0.2.3.e.8.7.y.2.0.0.2.3.0.0.ed
M|Laura Friedman|D|H-CA-30|||44|ea.5a.p.0.q.75.0.0.1.o.3.2.f.2.f.4.2.1.6.0.ee
M|Lateefah Simon|D|H-CA-12|||43|d9.c4.z.0.u.39.0.2.1.k.4.1.2.1.0.0.2.2.5.0.ef
M|Ayanna Pressley|D|H-MA-7|||43|en.20.5.0.a.0.c.1.1.27.5.4.0.5.0.0.2.5.0.0.eg
M|Clay Fuller|R|H-GA-14|||3y|dp.7s.25.0.q.2cw.q.0.0.4.1.0.14.2.0.0.2.0.0.0.eh
M|Greg Casar|D|H-TX-35|||3r|d0.dt.l.0.17.0.0.0.1.1e.7.1.20.e.0.0.2.2.0.0.ei
M|Michael Cloud|R|H-TX-27|||3q|dn.8a.1r.0.m.9.0.0.0.14.7.4.5.f.0.0.2.2.2.0.ej
M|Thomas P. Tiffany|R|H-WI-7|||3p|dy.6j.16.0.m.4.0.0.1.1c.a.4.i.4.0.0.2.3.8.0.ek
M|Herbert C. Conaway, Jr.|D|H-NJ-3|||3g|az.oe.3z.0.2a.0.e.0.0.k.0.5.0.4.0.0.2.1.0.0.el
M|LaMonica McIver|D|H-NJ-10|||3f|bn.jy.3j.0.1e.2.0.0.0.14.4.3.p.4.0.0.2.2.0.0.em
M|Aisha Wahab|D|H-CA-14|||35|ez.5.2.0.1.qc.27b.0.0.0.0.0.k.0.0.0.0.0.0.0.en
M|Josh Brecheen|R|H-OK-2|||2x|er.p.n.0.4.0.0.0.2.t.6.2.0.q.0.0.2.2.0.0.ep
M|Darline Graham|R|S-SC|||2g|b5.g5.30.75.s.0.0.0.0.i.0.0.0.0.0.0.0.0.0.0.er
M|Analilia Mejia|D|H-NJ-11|||2e|e5.5v.o.0.q.98.0.0.0.0.0.0.a.0.0.0.2.0.0.0.es
M|James C. Moylan|R|H-GU-0|||2c|et.0.z.0.0.0.0.0.0.17.9.4.5.2.0.0.3.1.d.0.et
M|Pablo José Hernández|D|H-PR-0|||1r|dd.au.1k.0.r.0.0.0.0.u.1.0.0.0.1.0.2.2.0.0.eu
M|Luz M. Rivas|D|H-CA-29|||1p|cy.cm.25.0.1e.0.0.0.0.9.4.0.4s.2.1.0.2.2.7.0.ev
M|James Gallagher|R|H-CA-1|||l|ef.3c.1h.0.a.0.0.0.0.g.0.0.1e.0.0.0.3.1.0.0.ew
M|Kimberlyn King-Hinds|R|H-MP-0|||l|eq.19.a.0.1.0.0.0.0.6.0.2.0.6.0.0.3.0.0.0.ex
M|Aumua Amata Coleman Radewagen|R|H-AS-0|||i|ev.5.e.0.1.0.0.0.0.5.0.c.0.0.0.0.3.3.13.0.ey
M|Everton Blair Jr.|D|H-GA-13|||7|eo.24.0.0.9.0.0.0.0.0.0.0.0.0.0.0.0.0.0.0.ez
L|Gregory Sunstrum|D|Brownstein Hyatt Farber Schrec|||ji|47.o9.6c.on.0.2sm.2j.1o.13.2u.p.3u.1h.2.0.0.2
L|Elizabeth Craddock|D|Holland & Knight LLP|||ji|48.m3.1ag.lv.0.36n.v.16.k.p.2.37.12.1.0.0.a.0.0.3.0.2
L|Timothy Molino|D|Tiber Creek Group|||ji|49.oy.1c.pw.0.4o2.y.3q.b.ou.z.ih.26.1.0.0.0.0.0.1.0.1.0.0.0.c
L|Jeanne Haggerty|R|Williams And Jensen, PLLC|||jh|4a.os.25.p6.0.2j3.18.19.d.e8.p.8l.2o.1.0.0.1e
L|Hazen Marshall|R|Marshall & Popp, LLC|||jg|4b.p4.u.q1.0.62w.11.2u.7.xv.12.ha.3f.1.0.0.0.0.1
L|William Dunham|R|Brownstein Hyatt Farber Schrec|||jg|4c.oq.2h.oq.0.21l.14.1r.q.8a.q.6w.1z.2.1
L|John Stipicevic|R|Cgcn Group, LLC|||jg|4d.nu.cn.oc.0.3o0.1n.9c.f.dc.t.dc.3u.1.0.0.0.1
L|Sean Richardson|D|Tiber Creek Group|||jf|4e.ne.kc.p0.0.3ww.x.2b.f.46.f.3q.0.2.0.0.0.0.0.0.0.0.0.0.0.a
L|Cynthia Brown|D|Forbes-Tate|||jf|4f.o2.9h.op.0.5pf.2e.3m.j.l2.13.6t.31.1.0.0.0.1
L|Stoney Burke|R|Aquia Group Inc.|||jf|4g.oh.3k.op.0.3on.10.1c.2.1a8.1k.bm.4x.2.0.0.0.0.0.0.0.3
L|Leslie Zelenko|D|Kountoupes Denham Carr & Reid|||jf|4h.ni.ig.ol.0.2mz.u.y.a.2v.h.48.c.2.0.0.a
L|Scott Nelson|M|K&L Gates, LLP|||jf|4i.nl.gu.nd.0.1aj.1c.2h.u.3mh.7g.dp.5e.1.0.0.z.1
L|Kathryn Mills|D|Monument Advocacy|||je|4j.od.4u.pa.0.2np.1c.y.r.dt.w.9n.13.1.0.0.26
L|Elizabeth Bennett|R|Forbes-Tate|||je|4k.mi.10h.og.0.24r.14.15.8.3f.i.a.1.4.0.0.0.0.1
L|Saathvik Alety|R|Federal Hall Policy Advisors|||je|4l.nl.gr.pv.0.3ke.1e.11.f.xo.1t.a.1.3
L|Leslie Pollner|D|Holland & Knight LLP|||je|4m.ns.di.o3.0.44g.1n.1i.w.6x.i.3h.17.2
L|Michael Smith|D|Cornerstone Government Affairs|||je|4n.od.4s.oy.0.5ic.1w.x.m.3gc.20.39b.n0.0.0.0.2i.2
L|Kelsey Griswold-Berger|R|Arentfox Schiff LLP|||je|4o.lj.1ks.n7.0.1kv.15.58.15.2m.4.5.2.1.5.0.0.1
L|Noah Marine|D|Invariant LLC|||jd|4p.o5.81.pm.0.3z0.w.1c.m.c2.v.14.r.2
L|Carlos Jackson|D|Cornerstone Government Affairs|||jd|4q.oc.57.pk.0.34a.w.z.b.f9.1e.4l.k.1.0.0.19.0.0.0.0.1
L|Timothy Hannegan|D|Penn Avenue Partners|||jc|4r.o7.79.os.0.577.1a.2q.v.14i.12.hi.4e.0.0.0.48.0.1.0.0.b
L|Madison Smith|R|Cozen O'Connor Public Strategi|||jc|4t.nz.ae.oo.0.37s.1k.q.17.4g.6.1v.k.3.1
L|Barry Lasala|D|Avoq, LLC|||jc|4u.o0.ab.ok.0.47w.1a.1l.7.kk.y.ak.3j.1.0.0.5.0.1
L|Bradford Cheney|D|The Majority Group, LLC|||jb|4v.os.24.pp.0.4f4.c.2.4.eg.t.9s.21.2.0.0.2w.0.1.0.0.2
L|Rosemary Gutierrez|D|Mehlman Consulting, Inc.|||jb|4w.mo.x5.o8.0.3kr.4i.ds.14.1d.a.1t.0.0.2.0.a
L|Keith Castaldo|D|Avoq, LLC|||jb|4y.oa.64.p4.0.3jm.14.17.h.5z.f.69.1w.2.0.0.0.0.0.0.0.1
L|Nicole Venable|D|Invariant LLC|||ja|4z.nk.hd.o3.0.2i5.v.19.h.j1.10.1ux.1m.1.0.0.26
L|Bart Stupak|D|Venable LLP|||ja|50.lw.1dx.ml.0.1h0.d.19.d.49.g.1e.2.0.0.2.a.1
L|Cheryl Jaeger|R|Crossroads Strategies, LLC|||ja|51.ng.jl.nm.0.20q.1z.3z.t.d0.o.4o.1n.1.2.0.0.0.0.0.1
L|Daniel Zawitoski|D|Tiber Creek Group|||ja|52.or.28.po.0.3rb.17.3d.e.eq.15.8c.2a.1.0.0.5.0.0.0.0.1
L|Dean Rosen|R|Mehlman Consulting, Inc.|||ja|53.nz.ah.oh.0.37s.3u.cx.13.wp.11.p1.53.0.0.0.19.0.0.1
L|Sean Joyce|R|Atlas Crossing LLC|||ja|54.ne.kp.ob.0.364.1y.3s.11.g1.12.2i.u.1.1
L|John Twomey|R|Tiber Creek Group|||j9|55.n3.pm.o1.0.2z3.x.2m.a.av.l.23.p.2
L|Thomas Koonce|D|Rich Feuer Anderson|||j9|56.or.29.pr.0.485.1e.5.9.f1.13.6z.1p.1.3.0.k
L|Mary Reid|R|Kountoupes Denham Carr & Reid|||j9|57.nb.lx.ol.0.3ij.14.1r.r.tr.1f.5c.3.2.0.0.0.0.0.0.1.1
L|Todd Bertoson|R|Capitol Hill Policy Group LLC|||j9|58.mw.st.o0.0.2s7.o.2l.p.fu.i.14.l.1.0.0.0.0.0.2.0.4
L|Jeff Mackinnon|R|Farragut Partners LLP|||j9|59.o2.9i.om.0.35i.20.p.a.1zf.30.nb.2y.1.1.0.a
L|Brittan Specht|R|Michael Best Strategies LLC|||j9|5a.mk.yz.nb.0.3w8.1z.v.s.k.3.11.9.0.s.0.0.0.0.0.0.9
L|Jeffrey Forbes|D|Forbes-Tate|||j8|5b.o8.6w.os.0.4cl.1p.2z.a.1be.1f.mg.7s.0.0.0.1m.1.0.0.0.0.0.0.0.1j
L|Brian McGuire|R|Brownstein Hyatt Farber Schrec|||j8|5c.p2.11.pe.0.4fk.34.1q.15.78.k.cy.2q.1.0.0.0.1
L|Janice Bashford|D|Arnold & Porter Kaye Scholer L|||j8|5d.nw.cb.nx.0.157.i.1k.h.ev.n.h6.2d.0.3.0.x.0.0.0.0.1
L|Joshua Teitelbaum|D|Akin Gump Strauss Hauer & Feld|||j8|5e.nz.ar.o2.0.3vm.13.h.f.52.10.6m.2f.2.0.0.2.1
L|Rick Murphy|R|Forbes-Tate|||j7|5f.nq.e8.ol.0.40t.1q.2z.f.qe.v.3w.1b.1.0.0.0.1
L|Mary Beal|R|Kountoupes Denham Carr & Reid|||j7|5g.ne.k7.pg.0.3pc.14.1g.f.8m.r.p.1.2
L|Kirsten Chadwick|R|Fierce Government Relations|||j7|5h.oa.5v.ov.0.4i5.2f.9j.x.2d0.27.ps.7f.0.0.0.5.0.2
L|Scott Shewcraft|D|Mindset Advocacy, LLC|||j7|5i.oa.5s.ph.0.44u.1t.n.n.9h.m.2g.11.1.0.0.z
L|Joseph Bushong|D|Invariant LLC|||j6|5j.mq.vw.ns.0.2s7.m.1k.o.19.5.4l.4.3.0.0.0.0.0.0.0.1
L|Michael Rogers|D|Greenberg Traurig, LLP|||j6|5k.o6.7n.p4.0.2wt.s.d.c.9o.c.12.h.2.0.0.c.0.0.0.0.0.0.0.0.7
L|Joel White|R|Horizon Government Affairs|||j6|5l.ni.il.nv.0.1ve.x.14.c.164.17.hi.4t.1.0.0.0.0.0.1.0.0.5.0.1
L|Katherine Monge|D|Capitol TAX Partners, LLP|||j6|5m.nm.gi.pa.0.3ha.14.j.5.6t.o.2s.1.1.1.0.f.0.0.0.0.1
L|Erik Olson|D|Venn Strategies|||j6|5n.mt.ui.nx.0.2nl.o.d.z.8u.y.1j.c.1.5.0.0.1.0.0.2.0.0.1.1
L|Harold Hancock|R|Brownstein Hyatt Farber Schrec|||j5|5o.o9.6b.oo.0.651.2d.1l.x.ia.z.2h.29.1.0.0.0.1
L|Charles French|M|Cozen O'Connor Public Strategi|||j5|5p.os.1y.py.0.505.1s.7.12.m7.1m.3x.1c.3.0.0.0.0.1
L|Mark Williams|R|Ferox Strategies|||j4|5q.nz.ak.o5.0.48z.19.8.m.7x.i.ih.1c.3.1.0.0.1.0.0.1.0.0.2.0.f
L|Joel Roberson|R|Holland & Knight LLP|||j4|5r.no.fc.no.0.44y.10.2j.x.3h.d.5f.2n.0.0.0.0.1.0.6
L|Zach Deatherage|R|Akin Gump Strauss Hauer & Feld|||j4|5s.mq.w2.n4.0.1w9.1n.1f.p.1u.2.18.p.5
L|John Green|R|Crossroads Strategies, LLC|||j4|5t.na.me.o6.0.2w9.1f.6z.v.gw.q.5f.f.0.0.0.3k.0.1.0.0.0.0.3
L|LEA Sulkala|D|Resolution Public Affairs, LLC|||j4|5u.nz.ap.o4.0.3fs.10.1o.5.ip.b.9n.36.1.1
L|Charles Cooper|R|Brumidi Group|||j4|5w.mc.14f.pg.0.4ir.p.2a.b.99.h.0.2.2.0.0.0.0.0.0.0.0.0.2
L|Chris Giblin|R|OGR|||j3|5x.ot.1u.pu.0.3d2.1f.48.p.13j.1r.6e.1n.1.0.0.2
L|Beau Schuyler|D|Thorn RUN Partners|||j3|5y.of.3y.oq.0.5bx.y.m.a.q9.13.g1.3i.0.2.0.p
L|Brady King|D|NVG, LLC|||j3|5z.lz.1ci.mv.0.17w.c.p.5.bu.1c.2k.5.6.0.0.1w.0.0.0.0.0.0.0.0.8
L|Constantine Hingson|R|Mehlman Consulting, Inc.|||j3|60.m5.18w.n8.0.26o.3o.9k.10.50.e.20.4.1.2
L|Michael Williams|D|The Williams Group|||j3|61.o8.6v.os.0.40o.x.1n.i.1oy.1y.lt.6k.0.0.0.9q.1
L|Jeffrey Billman|R|Axadvocacy Government Relation|||j3|62.nc.lf.oa.0.20p.u.11.9.5q.7.2s.o.4
L|Reginald Babin|D|Akin Gump Strauss Hauer & Feld|||j3|63.o0.a3.ob.0.1xg.11.r.i.3u.n.4b.1m.1.1.0.5.1.0.0.0.2
L|Maia Estes|D|Invariant LLC|||j2|64.nk.hk.o6.0.2fk.n.11.d.ns.1g.ct.1b.1.0.0.1o.0.0.0.0.1
K|Sanofi U.s.|U||||jw|2k.lgx.26.1i.0.4.0.0.4.3.2.3.c
K|American Academy Of Family Physicians|U||||jw|2l.azp.60.35.0.3.5.0.0.0.8.8.7
K|American Academy Of Pediatrics|U||||jv|2m.3c5.4h.2j.0.9.3.0.0.0.3.3.r
K|Nucor Corporation|U||||ju|2n.7ia.p.m.19.0.4.0.0.3.0.0.e
K|Associated General Contractors Of America|U||||jt|2o.2kv.5u.3g.0.c.3.0.0.0.6.8.m
K|Marathon Petroleum Corporation|U||||js|2p.9z6.1m.14.0.k.0.0.1.2.0.0.e
K|National Shooting Sports Foundation|U||||jr|2q.lon.78.35.b4.0.0.0.0.0.1.1.3
K|Occidental Petroleum Corporation|U||||jr|2r.xt5.4.3.9cy.4.0.0.0.0.0.0.i
K|Nuclear Energy Institute|U||||jr|2s.8r0.45.2f.i.1.7.0.0.0.2.2.a
K|Ncta, The Internet & Television Association|U||||jr|2t.1c8e.8j.3p.0.1.3.1f.0.0.0.0.f
K|CMS Energy Corp|U||||jr|2u.3ck.5l.3a.a.4.0.0.0.1.0.0.6
K|Solana Policy Institute|U||||jq|2v.45g.1l.1b.1dl.0.0.0.0.0.0.0.3
K|Walmart Inc|U||||jp|2w.ug8.1i.12.0.2.1.0.b.d.0.0.15
K|Novartis|U||||jo|2x.omc.45.22.z.0.1.0.2.2.0.0.g
K|American Heart Association|U||||jo|2y.4ce.6s.30.0.7.2.0.0.0.4.4.c
K|American Electric Power|U||||jn|2z.r3.5.4.28.6.3.0.6.c.0.0.7
K|Pepsico|U||||jn|30.gdg.12.r.0.3.0.0.w.o.0.0.i
K|Southern Environmental LAW Center|U||||jm|31.26m.2n.1m.0.i.3.0.0.0.2.2.9
K|Giffords|U||||jm|32.1c4.81.3u.5xl.0.0.0.0.0.0.0.6
K|Tesla|U||||jm|33.60t.j.d.0.a.1.0.c.a.1.1.g
K|T-Mobile USA Inc|U||||jm|34.13lu.24.1n.q.0.0.0.b.d.0.0.4
K|International Fresh Produce Association|U||||jm|35.563.2a.1r.0.7.2.0.0.0.0.0.f
K|National Association of Broadcasters|U||||jm|36.11ow.2m.1i.0.1.8.c.0.0.0.0.5
K|Transportation Trades Department AFL-CIO|U||||jl|37.4hj.1t.1a.0.3.b.0.0.0.2.2.n
K|Calportland Company|U||||jk|38.2oy.8.8.3m.5.0.0.0.0.0.0.f
K|Mortgage Bankers Association|U||||jk|39.9ow.4a.2d.0.2.c.0.0.0.0.0.c
K|Novo Nordisk Inc.|U||||jk|3a.nha.i.e.22.1.2.0.0.0.0.0.d
K|Independent Petroleum Association Of America|U||||jj|3b.22q.1v.x.0.7.7.0.0.0.0.0.7
K|Aerospace Industries Association Of America Inc|U||||jj|3c.5ws.1a.z.0.3.8.0.0.0.2.2.g
K|Earthjustice|U||||jj|3d.14y.77.3p.0.1u.5.0.0.0.1.a.6
K|Southwest Airlines|U||||ji|3e.66i.1b.q.2.3.1.0.1.2.0.0.b
K|Uber Technologies Inc.|U||||ji|3f.d2p.w.n.1t.0.0.0.3.5.0.0.e
K|Reproductive Freedom For ALL|U||||ji|3g.t6.50.2c.156.1.0.0.0.0.0.0.f
K|PHRMA|U||||jh|3h.7ia.n.h.7s.0.2.0.0.0.0.0.7
K|International Union Of Operating Engineers|U||||jh|3i.1h5.1h.11.cqk.0.0.0.0.0.0.0.8
K|Motion Picture Association|U||||jh|3j.9u6.1u.1e.a.0.3.g.0.0.0.0.8
K|National Milk Producers Federation|U||||jg|3k.4dm.1z.19.0.3.5.0.0.0.2.2.e
K|Cummins Inc.|U||||jg|3l.9ii.21.1b.0.3.0.0.2.3.0.0.m
K|National Association For GUN Rights|U||||je|3m.302.8d.44.5z.0.1.0.0.0.0.0.3
S|Earn International Union Of Operating Engineers|U|super PAC||||0.3fpq
C|Republican National Committee|R|party national committee||||lci.1n
C|Grow The Majority|R|joint fundraising committee||||457.13
N|The PAC for America's Future|U|527 political org||||1qx9
N|National Rural Water Association|U|501(c)(6)||||13et
F|Taipei Economic and Cultural Representative Offi|U|TAIWAN||||5r
A|HUD|U|Executive agency||||3az
A|FCC|U|Executive agency||||2gs
A|FTC|U|Executive agency||||222
A|CFPB|U|Executive agency||||1fj
H|House Committee on Ethics|U|HSSO||||a
H|House Select Subcommittee to Investigate the Rem|U|HSQJ||||7
B|National Association Of Realtors|U|Form 3L bundler||||6u
`;
const EA0 = [
"8k.22.0.2bc 8k.n.0.2bc 8k.4a.0.2bc 8l.4j.0.g7c 8l.4h.0.ct4 8l.4g.0.ccg 8m.25.0.7ps 8m.4a.0.5sc 8m.3e.0.50k 8n.1f.0.weo 8n.v.0.i4s 8n.70.0.hwg 8o.56.0.5sc 8o.2g.0.3uw 8o.3t.0.2p8 8p.l.0.8hk 8p.e.0.6ek 8p.i.0.60o 8q.53.0.6k4 8q.22.0.5sc 8q.67.0.5sc 8r.1k.0.a6o 8r.25.0.5eg 8r.22.0.4mo 8s.3n.0.5sc 8s.2h.0.438 8s.3.0.1xg 8t.32.0.6k4 8t.31.0.3uw 8t.3t.0.2w6 8u.1l.0.6k4 8u.31.0.334 8u.3u.0.1jk 8v.1l.0.kak 8v.4h.0.ei8 8v.3r.0.5sc 8w.4h.0.8kc 8w.3r.0.7ps 8w.5j.0.4mo 8x.u.0.g7c 8x.49.0.f8m 8x.2b.0.7ps 8y.3k.0.af0 8y.4h.0.7ps 8y.34.0.6k4 8z.i.0.f8m 8z.1n.0.7ps 8z.j.0.668 90.1l.0.n8o 90.31.0.7ps 90.76.0.3vg 91.7g.0.668 91.78.0.48s 91.25.0.3uw 92.4h.0.48s 92.2g.0.2p8 92.3t.0.2bc 93.3k.0.bko 93.4h.0.99c 93.31.0.4mo 94.4h.0.d48 94.1l.0.7bw 94.p.0.3h0 95.3t.0.67m 95.9.0.2bc 95.22.0.1xg 96.3r.0.6r2 96.2.0.4mo 96.3a.0.4fq 97.u.0.uv4 97.1f.0.bko 97.16.0.9n8 98.31.0.bko 98.32.0.bko 98.11.0.bhw 99.53.0.9lc 99.11.0.6gn 99.25.0.60o 9a.u.0.e4c 9a.4u.0.668",
"9a.16.0.2bc 9b.31.0.a14 9b.7o.0.3uw 9b.54.0.1yc 9c.2g.0.naw 9c.4h.0.i20 9c.7m.0.8vg 9d.1e.0.4mo 9d.4h.0.2p8 9d.1l.0.2p8 9e.u.0.k50 9e.12.0.ew4 9e.2k.0.aq4 9f.25.0.48s 9f.78.0.48s 9f.4t.0.3h0 9g.1r.0.4mo 9g.5u.0.3uw 9g.2n.0.3h0 9h.7d.0.n5c 9h.21.0.gz4 9h.7i.0.ftg 9i.4h.0.7ps 9i.5i.0.1jk 9j.2.0.48s 9j.z.0.3h0 9j.59.0.334 9k.44.0.7wq 9k.32.0.7ps 9k.11.0.7eo 9l.a.0.1jk 9l.4h.0.1jk 9l.3t.0.1jk 9m.1.0.di4 9m.16.0.c6w 9m.1m.0.asw 9n.i.0.a3w 9n.m.0.70s 9n.3c.0.3uw 9o.1l.0.bt0 9o.31.0.5sc 9o.5k.0.5eg 9p.4e.0.jg0 9p.11.0.b9k 9p.10.0.6ek 9q.26.0.5sc 9q.a.0.4s8 9q.22.0.3uw 9r.1g.0.7ps 9r.e.0.6k4 9r.12.0.668 9s.u.0.1xg 9s.3n.0.1jk 9s.12.0.1jk 9t.n.0.668 9t.p.0.668 9t.38.0.5hx 9u.k.0.2et 9u.1f.0.2bc 9u.2m.0.1xg 9v.3g.0.2bc 9v.25.0.1xg 9w.1f.0.k28 9w.1n.0.jag 9w.12.0.jag 9x.5i.0.99c 9x.n.0.7sk 9x.44.0.6k4 9y.6d.0.e21 9y.0.0.86g 9y.1o.0.83o 9z.31.0.cqc 9z.1l.0.byk 9z.3k.0.asw a0.4t.0.3uw a0.31.0.2p8 a0.7n.0.1yz a1.u.0.d48 a1.7.0.9vk a1.4m.0.6y0",
"a2.5o.0.2bc a2.5y.0.1xg a2.7j.0.1jk a3.1z.0.86g a3.12.0.6sg a3.16.0.5ms a4.7.0.6ek a4.61.0.5eg a4.4c.0.48s a5.4b.0.334 a5.2z.0.1jk a6.12.0.bt0 a6.20.0.41u a6.s.0.2bc a7.1f.0.7ps a7.12.0.7bw a7.1.0.4mo a8.1n.0.3jw a8.4z.0.2p8 a8.3.0.1xg a9.2g.0.nzw a9.4j.0.ir0 a9.31.0.fz0 aa.k.0.11yo aa.35.0.cvw aa.61.0.bt0 ab.11.0.aq4 ab.5m.0.9n8 ab.32.0.7ps ac.2g.0.7ps ac.4h.0.668 ac.6p.0.3uw ad.s.0.9n8 ad.2a.0.9ew ad.1r.0.9aq ae.25.0.2p8 ag.2g.0.cvw ag.53.0.a8r ag.n.0.9n8 ah.r.0.joc ah.1f.0.ipm ah.8.0.gmm ai.5n.0.1jk ai.2e.0.1jk ai.3h.0.1jk aj.1n.0.af0 aj.1h.0.8vg aj.i.0.7bw ak.2v.0.af0 ak.1a.0.60o ak.z.0.53c al.i.0.jzg al.23.0.c1c al.2a.0.a9g am.l.0.ffk am.s.0.9n8 am.2a.0.8n4 an.l.0.iio an.2a.0.9n8 an.1g.0.8hk ao.64.0.1jk ap.u.0.9n8 ap.v.0.2bc ap.3i.0.1xg ar.z.0.asw ar.i.0.ac8 ar.1n.0.a14 as.2l.0.hd0 as.g.0.668 as.m.0.3h0 at.3e.0.f0a at.4h.0.6y0 at.1l.0.58w au.0.0.50k au.j.0.1jk au.e.0.1jk av.35.0.1xg aw.12.0.93s aw.t.0.4h4 aw.3x.0.3uw",
"ax.9.0.3uw ax.1v.0.30c ax.13.0.2bc ay.1l.0.3uw ay.4h.0.334 ay.2g.0.2bc az.1j.0.3l6 az.q.0.2p8 az.37.0.1qi b0.0.0.asw b0.3c.0.asw b0.3o.0.93s b1.n.0.7y4 b1.27.0.41u b1.45.0.3uw b2.q.0.9n8 b2.1n.0.92e b2.2k.0.8c0 b3.1l.0.a14 b3.31.0.8c0 b3.44.0.6bs b4.67.0.5eg b4.r.0.1xg b4.1c.0.1jk b5.1.0.mzs b5.5.0.i20 b5.u.0.hz8 b6.1l.0.ay3 b6.2e.0.58w b6.5r.0.2bc b7.5u.0.2bc b7.27.0.1xg b8.11.0.7hg b8.a.0.70s b8.10.0.53c b9.16.0.bko b9.1r.0.6sg b9.s.0.4mo ba.6u.0.3h0 ba.3c.0.2jo bb.3h.0.6ek bb.53.0.5ms bb.4h.0.3wf bc.0.0.j7o bc.z.0.ct4 bc.2m.0.6mw bd.2.0.1jk be.1s.0.3ny be.45.0.2cq be.4h.0.24e bf.e.0.af0 bf.12.0.8y8 bf.16.0.4mo bg.13.0.2p8 bg.o.0.2bd bg.6.0.1xg bh.2.0.6li bh.2f.0.4mo bh.2r.0.48s bi.4q.0.a3w bi.3x.0.93s bi.2h.0.70s bj.56.0.7bw bj.5g.0.50k bj.26.0.1xg bk.6t.0.8hk bk.1l.0.6y0 bk.4h.0.1xg bl.2b.0.a14 bl.1f.0.3uw bl.e.0.334 bm.n.0.1jk bn.4o.0.2p8 bn.4b.0.2bc bn.5e.0.1jk bo.7n.0.1jk bp.j.0.mrg bp.4n.0.i7k bp.16.0.ei8 bq.l.0.5eg"
].join(" ");
const EA1 = [
"bq.1.0.4tm bq.1a.0.48s br.1n.0.2p8 br.2l.0.2bc br.i.0.2bc bs.4j.0.bko bs.4h.0.8hk bs.1l.0.6k4 bt.1l.0.jwo bt.4j.0.iio bt.4h.0.ei8 bu.s.0.7bw bu.k.0.5eg bu.1f.0.5eg bv.e.0.690 bv.1r.0.4s8 bv.2l.0.4mo bw.4g.0.2p8 bx.5c.0.a3w bx.r.0.8y8 bx.3t.0.7ps by.n.0.a14 by.10.0.6r2 by.6.0.48s bz.7u.0.334 bz.2w.0.1jk c0.3r.0.9n8 c0.2g.0.8kc c0.3t.0.7r6 c1.54.0.334 c1.53.0.1jk c1.6j.0.1jk c2.l.0.di4 c2.1g.0.7ps c2.68.0.7ps c3.i.0.4mo c3.37.0.48s c3.2m.0.3bg c4.1o.0.48s c4.3q.0.334 c5.1l.0.99c c5.11.0.334 c5.4h.0.1xg c6.22.0.8hk c6.31.0.334 c6.n.0.2bc c7.i.0.2bc c8.23.0.2bc c8.4q.0.1xg c8.0.0.1jk c9.l.0.50k c9.1n.0.4mo c9.4x.0.2w6 ca.4h.0.1qi ca.6j.0.1jk ca.1l.0.1jk cc.55.0.7t9 cc.s.0.5sc cc.i.0.53c cd.5m.0.83o cd.32.0.7ps cd.44.0.668 ce.4.0.5sc ce.z.0.4pg ce.2h.0.1jk cf.1d.0.q5o cf.6.0.c6w cf.28.0.7ps cg.12.0.8pw cg.3n.0.7wq cg.7b.0.50k ch.4h.0.334 ch.1l.0.1xg ch.52.0.1xg ci.6w.0.7ps ci.85.0.7iu ci.2e.0.4mo cj.1.0.5sc cj.4k.0.4mo cj.3a.0.48s",
"ck.1l.0.iha ck.31.0.4mo ck.3e.0.48s cm.4d.0.4mo cm.l.0.334 cn.k.0.334 cn.q.0.2p8 cn.5.0.2p8 co.11.0.dno co.22.0.70s co.2m.0.4mo cp.7g.0.1jk cq.12.0.avo cq.42.0.a9g cq.2.0.7k8 cr.4q.0.8vg cr.7a.0.334 cr.3x.0.334 cs.2g.0.asw cs.1l.0.7lm cs.64.0.5eg ct.a.0.jd8 ct.5i.0.a6o ct.6h.0.8it cu.m.0.3uw cv.l.0.asw cv.40.0.5eg cv.29.0.2p8 cw.b.0.ct4 cw.3w.0.9vk cw.6f.0.9q0 cx.e.0.c8a cx.8f.0.3h0 cx.7d.0.2te cy.i.0.1xg cz.3e.0.48s cz.1l.0.334 cz.10.0.2p8 d0.6q.0.334 d0.61.0.334 d0.4c.0.2ia d1.b.0.cks d1.1d.0.6sg d1.5p.0.6jf d2.52.0.6r2 d2.5y.0.4mo d2.2x.0.48s d4.4.0.8vg d4.4x.0.7iu d4.d.0.6k4 d5.z.0.anc d5.2m.0.7k8 d5.36.0.7bw d6.1l.0.6oq d6.1q.0.668 d6.3j.0.5sc d7.s.0.b16 d7.16.0.8vd d7.u.0.5sc d8.1p.0.cmv d8.83.0.83o d8.3f.0.3uw d9.3o.0.60o db.13.0.3uw db.12.0.3uw db.1n.0.2bc dc.3o.0.4fq dc.2i.0.2bc de.5x.0.7jv de.5.0.5eg de.36.0.3uw df.21.0.2p8 dg.3m.0.asw dg.1i.0.aq4 dg.7.0.5eg dh.s.0.1xg di.9.0.guy di.s.0.7wq di.6p.0.2w6 dj.2g.0.1jk",
"dl.u.0.1xg dl.5a.0.1jk dl.2r.0.1jk dm.59.0.1jk dr.6.0.1jk dt.3u.0.4mo dt.53.0.4ht du.17.0.byk du.7l.0.9n8 du.47.0.7ps dw.5d.0.vmw dw.7f.0.t38 dw.l.0.kg4 dx.1j.0.8pw dy.1t.0.334 dy.7y.0.1jk dz.2.0.99c dz.0.0.668 dz.1t.0.5eg e1.68.0.3h0 e1.4k.0.1xg e3.4q.0.3uw e3.5a.0.334 e4.2g.0.zhs e4.4h.0.a14 e4.64.0.41u e5.2k.0.1xg e5.7f.0.1jk ea.24.0.ftg ea.4j.0.ffk ea.2l.0.ei8 ec.7n.0.5sc ec.t.0.48s ec.2n.0.3h0 ef.76.0.6li ef.6x.0.6d6 ef.4l.0.5bo el.16.0.5eg el.6u.0.42k el.9.0.3h0 em.13.0.1xg er.16.0.83o er.3a.0.3uw er.4u.0.3h0 8n.1a.1.kd 8n.2.1.gi 96.1f.1.9w 96.3a.1.9f 97.1f.1.cz 98.31.1.99 98.1k.1.8q 9d.2a.1.7p 9e.1f.1.t7 9e.k.1.d0 9p.10.1.c5 9p.u.1.9v 9t.4h.1.89 9t.3t.1.7v 9w.1f.1.12w 9w.3p.1.83 9z.1w.1.8h a8.25.1.e6 a8.l.1.dy aa.k.1.jg aa.7e.1.fu ab.a.1.b3 ab.r.1.7j ah.r.1.bd ah.4m.1.99 aj.1g.1.93 aj.17.1.85 ak.1f.1.bt am.s.1.8k an.28.1.7l as.k.1.jr as.7e.1.fu b2.1g.1.aj b2.17.1.91 b5.19.1.d0 b5.3p.1.cu",
"bi.2h.1.8i bl.2b.1.co bl.2z.1.a6 bp.1b.1.9i bp.6.1.9a bq.12.1.e9 bq.y.1.9r bu.1f.1.jg cr.l.1.71 cr.4.1.70 cs.2a.1.7p cw.2a.1.9y cw.5p.1.82 cy.1c.1.96 cy.3b.1.8y cz.2a.1.7p d1.2a.1.80 di.9.1.8j dn.19.1.a5 dn.1.1.94 du.47.1.au du.17.1.au dw.40.1.9w dw.3a.1.9e ec.8.1.7r ec.7n.1.72 er.4u.1.1wi er.35.1.xq ev.2r.1.d6 ev.5.1.8p 8k.n.2.1f8 8l.4j.2.7e7 8n.3.2.jfh 8o.2g.2.3ix 8p.12.2.2ai 8q.53.2.2sz 8r.a.2.3t5 8s.3n.2.20v 8t.25.2.1mr 8v.4h.2.2sk 8w.4h.2.4qx 8x.u.2.270 8y.4h.2.5l3 8z.35.2.ze 91.7r.2.2bv 92.4h.2.28g 93.4h.2.5l3 94.4h.2.6ub 96.53.2.14e 97.u.2.24q 98.53.2.6k8 99.53.2.53q 9a.4u.2.3hx 9c.4h.2.b26 9d.4h.2.3cn 9e.12.2.4l1 9f.25.2.1wj 9h.2n.2.1ww 9j.2.2.1ns 9k.32.2.282 9m.2a.2.3ze 9n.60.2.1rb 9p.10.2.3d1 9t.53.2.2eu 9w.2l.2.7jd 9x.a.2.1i5 9y.3.2.1pr 9z.4h.2.7jh a1.2a.2.2ve a3.12.2.3sz a4.7.2.14g a7.8.2.1zy a9.2g.2.f8p aa.i.2.1ex ab.a.2.3b3 ac.4h.2.3wr ad.2a.2.1q1 ag.53.2.314 aj.3.2.161 ak.1p.2.398"
].join(" ");
const EA2 = [
"al.2a.2.441 am.2a.2.2cu an.2a.2.4vj ar.g.2.180 as.2l.2.bew at.4h.2.3wr aw.12.2.2ai ax.4.2.zu ay.4h.2.z6 b1.n.2.5h2 b4.67.2.1g6 b5.g.2.320 b6.3l.2.16h b8.a.2.297 b9.2a.2.1tf bb.53.2.2eu bc.3.2.3ml be.4h.2.1ea bf.4.2.zu bh.2.2.2tv bi.2h.2.32n bp.2a.2.1uh bq.1a.2.1rn br.2l.2.1j1 bs.4h.2.5l3 bt.4j.2.5t5 bu.1f.2.1if bv.2l.2.17y bx.4o.2.3r8 by.n.2.269 c5.4h.2.1ea c9.2l.2.so cc.2.2.1vx cd.32.2.1c2 ce.4.2.2hl cf.1d.2.270 cg.2n.2.13d ch.4h.2.148 ci.2g.2.1mf cj.4u.2.2bp cq.3.2.2qb ct.7.2.2g2 cu.m.2.wf cw.2.2.2cw cy.i.2.1jg cz.a.2.25n d1.5a.2.5fy d4.5.2.1vl d8.1p.2.7ap dg.7.2.1km dt.53.2.1yo dz.1t.2.ccs e1.35.2.ze ef.4o.2.3y0 8k.js.3.3ls8 8l.jt.3.3o3k 8m.k1.3.5lp 8n.jr.3.3r14 8o.jz.3.eg0 8p.jr.3.1063 8q.js.3.99c 8r.js.3.ffk 8s.jr.3.bko 8t.jz.3.eg0 8u.k1.3.7oe 8v.js.3.5le 8w.jt.3.6324 8x.k8.3.1jk 8y.k4.3.7ps 8z.jr.3.3dj 90.js.3.asw 91.jt.3.5sc 92.jz.3.eg0 93.k4.3.7ps 94.k4.3.99c 95.js.3.af0 96.j1.3.1cm 97.jw.3.bko 98.js.3.a14 99.js.3.2p8",
"9a.jw.3.rs 9b.jt.3.3uw 9c.k4.3.e9w 9d.k7.3.8hk 9e.jw.3.jag 9f.jt.3.rs 9g.jt.3.1jk 9h.ju.3.n6u 9i.js.3.2bc 9j.jr.3.ffk 9k.k6.3.2xk 9l.js.3.1aao 9m.k3.3.80w 9n.jx.3.2mg 9o.js.3.334 9p.js.3.3p1m 9q.js.3.1b2g 9r.jw.3.1jk 9s.jz.3.4y2 9t.k1.3.ens 9u.jz.3.bzc 9v.js.3.2p8 9w.jr.3.x5c 9x.js.3.l0y 9z.js.3.iio a0.js.3.8hk a1.jx.3.99c a3.ju.3.bko a4.k5.3.bko a5.js.3.a14 a7.jr.3.n5c a8.jr.3.fk5 a9.j2.3.2cvk aa.jx.3.1aao ab.js.3.2bc ac.k4.3.5eg ad.jr.3.k96 ae.js.3.5sc af.js.3.rs ag.j1.3.g7c ah.ju.3.bko ai.jt.3.dw aj.jr.3.ffk ak.jy.3.ffk al.jr.3.cqc am.jr.3.xra ao.jt.3.go aq.k0.3.rs ar.jr.3.wb7 as.jr.3.4c9 at.js.3.83o au.k8.3.rs av.jr.3.4iz aw.jr.3.94m ax.k8.3.1jk ay.jt.3.2yi b0.ju.3.5sc b1.k6.3.rs b3.js.3.3khq b4.k4.3.dw b5.jr.3.uv4 b6.jt.3.2w6 b7.jt.3.15o b8.js.3.2s00 b9.jx.3.7ps ba.k8.3.rs bb.jt.3.vep bc.jr.3.3jgu bd.jz.3.eg0 be.k4.3.1xg bf.k8.3.1jk bg.jw.3.rs bh.jr.3.8vg bi.jr.3.twe bj.jt.3.1xg bl.k8.3.dw bm.js.3.rs bn.js.3.aly bo.j1.3.d8e bp.k3.3.cyo",
"bq.ju.3.3uw br.jr.3.di4 bs.k4.3.7ps bt.jt.3.3778 bu.jw.3.bko bv.jr.3.a4l bw.jt.3.yq bx.k0.3.8hk by.jv.3.1jk bz.k2.3.1jk c0.jt.3.7bw c1.k0.3.rs c2.ju.3.5k0 c3.jr.3.kqj c4.jr.3.3uw c5.jt.3.4mo c6.jz.3.eg0 c7.jr.3.6r2 c9.jr.3.9ga ca.j1.3.1xg cb.ju.3.15o cc.jr.3.o42 cd.js.3.wsk ce.k8.3.3uw cf.jz.3.eg0 cg.k3.3.48s ch.js.3.3fsy ci.jt.3.rs cj.jw.3.rs ck.jt.3.2bc cl.js.3.1jk co.js.3.3uw cq.jr.3.10ng cr.jr.3.7ps cs.js.3.bko ct.ju.3.3uw cv.jz.3.cu8 cw.jr.3.1uyf cz.js.3.ga4 d1.jr.3.249u d2.jx.3.1xg d3.j1.3.1xg d4.jr.3.crd d5.jr.3.nmp d6.k7.3.6k4 d7.k3.3.4h4 d8.ju.3.jag da.k5.3.6ln dc.jx.3.1xg dd.k3.3.dw de.ju.3.15o di.ju.3.ffk dj.k2.3.rs dk.k1.3.uk dl.jw.3.rs dr.jt.3.dw ds.k5.3.2b0 dz.ju.3.yq0 e1.k7.3.2es e4.jt.3.1nyc e5.k6.3.2bc eb.js.3.15o ef.jv.3.1jk em.k8.3.dw j1.1w.4.ffk j1.6x.4.ffk j1.2x.4.bko j1.64.4.b6s j2.2u.4.ffk j2.64.4.ffk j2.7k.4.bko j2.15.4.bko jr.23.4.1bu8 jr.f.4.1bu8 jr.4u.4.1bu8 jr.59.4.1bu8 js.32.4.1bu8 js.1w.4.1bu8 js.x.4.1bu8 js.53.4.18lk",
"jt.2u.4.ecr jt.78.4.awr jt.64.4.ad2 jt.5s.4.9pt ju.8.4.ffk ju.1b.4.ffk ju.3p.4.ffk ju.2j.4.ffk jw.1f.4.lfls jz.23.4.b6s jz.2.4.b6s jz.u.4.af0 jz.1f.4.a14 k1.4h.4.ffk k1.3t.4.den k1.2g.4.bko k1.s.4.af0 k5.24.4.ens k5.3t.4.di4 k5.23.4.asw k5.11.4.asw k7.2a.4.a5j k7.5p.4.6dt k7.3i.4.3oz k7.4u.4.3of 92.jz.5.1 95.k5.5.1 9t.k1.5.1 q3.a.6.137gx q3.1s.6.z00y q3.54.6.x6wy q4.57.6.73h6 q4.c.6.6nea q4.5l.6.11ji q5.n.6.1c84 q7.25.6.pgo db.q7.7.1 f1.q6.7.1 8k.gu.8.2iks 8k.gn.8.24f2 8l.hx.8.4lw8 8l.fy.8.42bv 8m.i1.8.81co 8m.ga.8.5km8 8n.hz.8.aadc 8n.g8.8.a5vb 8o.fp.8.4r0r 8o.fv.8.48ia 8p.gm.8.c4ll 8q.gj.8.4i1c 8q.g0.8.3a6n 8r.ga.8.7ohp 8r.g3.8.39o4 8s.fv.8.4e6g 8s.gq.8.2wxs 8t.i0.8.1web 8t.fp.8.1ja3 8u.gl.8.6ac5 8u.ga.8.57r9 8v.hh.8.33gc 8v.h2.8.2qdo 8w.gm.8.c4ll 8w.i2.8.5fh1 8x.ge.8.28qr 8x.fr.8.20ni 8y.gf.8.53n4 8y.gd.8.4ozc 8z.hh.8.2gqg 90.fr.8.20ni 90.h8.8.1321 91.gq.8.8uac 91.hs.8.6z5o 92.i4.8.3k7r 92.fv.8.2v9k 93.h3.8.38h4 93.gq.8.314l 95.hm.8.44j8 95.h1.8.3e65 97.gf.8.53n4 97.gd.8.4ozc"
].join(" ");
const EA3 = [
"98.gr.8.2hfz 98.hx.8.1y8m 99.fx.8.p2s 99.gu.8.557 9a.gu.8.3lmo 9a.gn.8.1eup 9b.hh.8.33gc 9b.h2.8.2qdo 9c.hs.8.9i2t 9c.ga.8.7e7c 9d.g7.8.2i42 9d.hx.8.255s 9e.i4.8.40b4 9e.hx.8.3rgc 9f.hh.8.33gc 9f.h2.8.2qdo 9i.hg.8.5w6w 9i.g6.8.4w6l 9j.fv.8.48ia 9j.ga.8.1bu8 9k.ga.8.5sc0 9l.gd.8.2j5u 9m.gf.8.41u0 9m.gu.8.3tcg 9n.gu.8.zhs 9n.hn.8.tkt 9o.g6.8.33a6 9o.gr.8.2hfz 9q.gq.8.8uac 9q.gn.8.3fgg 9r.i0.8.7xhs 9r.fy.8.4dwj 9s.fv.8.tqp 9t.hh.8.3p0d 9t.fz.8.2412 9u.i4.8.2h0d 9u.fp.8.kxz 9v.fr.8.20ni 9v.h8.8.1321 9w.gv.8.4dnx 9w.hz.8.48e4 9x.g7.8.2ve8 9x.ge.8.2jkb 9y.i1.8.bn8l 9y.hs.8.78f0 9z.gs.8.7s3c 9z.fq.8.7023 a0.hw.8.39ng a0.ge.8.28qr a1.gf.8.41u0 a1.gu.8.3tcg a3.go.8.1aao a6.gu.8.2iks a6.gh.8.2g6m a7.gq.8.77rv a7.ft.8.59xb a9.hx.8.6c9l a9.gn.8.5zen aa.gd.8.3x2a aa.gr.8.3n68 ac.gy.8.5zbc ac.fw.8.36pn ad.fp.8.432z ad.hh.8.33gc ae.hu.8.2bjy ae.gv.8.1ezb af.fr.8.1002 af.g6.8.rqg ag.h2.8.2wt5 ai.g1.8.bko aj.hs.8.601s aj.g0.8.2u9w ak.hn.8.3dmz ak.fv.8.2g88 al.gd.8.42ls al.h3.8.13bc am.he.8.7ux7 am.i5.8.7i28 an.gd.8.42ls an.h3.8.33by",
"ao.h5.8.7i28 ao.h9.8.6uww ap.fv.8.4e6g ap.gq.8.2wxs ar.gs.8.4fa5 ar.i0.8.3vpr as.h9.8.2x4y as.i1.8.2r19 at.hx.8.4lw8 at.gw.8.4i1c au.gr.8.3674 av.gh.8.300w av.ga.8.25ya aw.hd.8.892g aw.hx.8.255s ay.g3.8.39o4 ay.g7.8.177k az.ga.8.7tmw az.fy.8.3udh b0.gf.8.41u0 b0.gu.8.3tcg b1.gp.8.1sat b2.hv.8.uv4 b3.hd.8.g2pc b3.gw.8.97sg b5.fq.8.3lmo b5.h3.8.3g6w b6.gy.8.5zbc b6.fw.8.kkr b7.hg.8.4l4g b7.fu.8.456d b8.h3.8.3g6w b8.hx.8.2p02 b9.g6.8.33a6 b9.gw.8.2pkn ba.h0.8.4lw8 bb.ge.8.28qr bb.fr.8.20ni bc.gj.8.4i1c bc.g0.8.3a6n bd.fv.8.48ia bd.hn.8.3dmz bf.g6.8.2p80 bf.hi.8.20lr bg.i4.8.2nhi bg.fx.8.hd0 bh.hs.8.6fhc bi.gf.8.5jl7 bi.hg.8.190d bj.gn.8.24f2 bj.hh.8.1pp6 bk.g3.8.39o4 bk.g7.8.177k bl.fy.8.4dwj bl.gv.8.2v2b bm.gq.8.2dz9 bm.fu.8.1sxz bn.gj.8.116q bo.gn.8.3563 bo.hg.8.11ug bp.hl.8.3udh bp.hh.8.3p0d br.h5.8.57i0 br.hx.8.3rsw bs.i4.8.2nhi bs.gu.8.2a12 bt.g0.8.4a8x bt.ht.8.1lvc bu.gv.8.255s bu.i1.8.1aao bv.g6.8.33a6 bv.gr.8.2hfz bw.hw.8.2d8s bw.fr.8.20ni bx.ht.8.7bmr bx.fv.8.39q3 c0.gn.8.5cwg c0.hx.8.4jys c1.i4.8.2nhi c1.fv.8.cuz",
"c2.hg.8.1vf9 c2.gj.8.11al c3.g3.8.9n80 c3.h3.8.72mo c4.hw.8.31xo c4.fr.8.20ni c5.fq.8.40oc c5.gn.8.1y7u c6.fv.8.48ia c6.hv.8.3785 c7.hl.8.2qib c7.hh.8.1x2s c8.fy.8.4dwj c8.hu.8.37ym c9.i1.8.bn8l c9.hs.8.6l9o ca.fr.8.20ni ca.h8.8.1321 cb.hh.8.462s cb.gd.8.20at cc.hk.8.8qat cd.hg.8.23m8 cd.go.8.1aao ce.hd.8.5ln9 ce.gn.8.43w3 cf.hn.8.111c cf.i5.8.5if cg.hg.8.1vf9 cg.gc.8.w5f ch.hx.8.2wfx ch.g7.8.2aaz cj.gu.8.2a12 cj.h8.8.27uc ck.fq.8.3lmo ck.hh.8.37qo cl.gr.8.2hfz cl.hx.8.1y8m cm.fq.8.3lmo cm.h3.8.3g6w cn.fy.8.155h cn.i5.8.kkr co.g1.8.35t8 cp.ga.8.1zc7 cp.hp.8.1tqm cq.ga.8.2w60 cq.gl.8.2r0t cr.ft.8.5w6w cs.g7.8.2i42 cs.gl.8.244e cv.fp.8.4r0r cv.fv.8.40si cw.ft.8.29sg cw.hp.8.1j45 cy.fr.8.3ts3n cz.hp.8.6idu cz.hd.8.3i11 d3.h9.8.8ezf d4.hs.8.437a d4.g3.8.2oq5 d5.gw.8.30xf d5.hx.8.2azg da.gj.8.13lx dd.gu.8.2tuo dd.gf.8.2tuo de.g6.8.4abk de.hg.8.3uw0 df.ga.8.ffk do.i4.8.3dww do.gp.8.2w60 e1.hb.8.1xg0 em.gn.8.4eq f1.g1.8.47ai fp.pl.9.8 fp.pp.9.d fr.p2.9.4 fr.p3.9.9 fr.p5.9.4 fr.pa.9.8 fr.pe.9.4 fr.ps.9.4",
"fr.pu.9.b fs.pd.9.2 ft.pk.9.2 fy.p2.9.a fy.p3.9.f fy.p4.9.f fy.p5.9.c fy.p7.9.a fy.p9.9.a fy.pa.9.f fy.pb.9.c fy.pc.9.b fy.pd.9.6 fy.pe.9.7 fy.pg.9.9 fy.ph.9.g fy.pk.9.8 fy.pm.9.3 fy.pn.9.8 g1.pd.9.3 g2.pi.9.4 g3.p1.9.p g3.p9.9.4 g6.pf.9.2 ga.p1.9.s ga.p9.9.6 ga.pr.9.4 ga.pt.9.5 gd.pb.9.5 gd.pr.9.4 gj.p6.9.7 gk.p6.9.7 gk.pi.9.4 gk.pj.9.7 gk.pm.9.5 gn.p2.9.6 gn.p4.9.5 gn.p5.9.6 gn.p7.9.6 gn.p9.9.5 gn.pb.9.7 gn.pc.9.6 gn.pd.9.4 gn.pe.9.4 gn.pg.9.6 gn.pj.9.7 gn.pk.9.4 gn.pn.9.3 gn.pu.9.7 gt.p8.9.8 gt.pb.9.5 gt.pc.9.4 gt.pg.9.5 gt.ph.9.8 gt.pm.9.3 gt.pq.9.2 gt.pr.9.5 gv.ps.9.4 gw.pp.9.j gx.pk.9.2 gx.pn.9.3 gx.pq.9.2 gx.pt.9.3 gz.ph.9.6 gz.pn.9.6 h0.p6.9.6 h0.pi.9.4 h0.po.9.5 h3.p1.9.l h3.p8.9.6 h3.pc.9.5 h3.pg.9.4 h3.pi.9.6 h3.pl.9.g h3.pm.9.3 h3.pp.9.w h3.pq.9.2 h3.pr.9.4 h3.pt.9.5 h3.pu.9.5"
].join(" ");
const EA4 = [
"h5.pf.9.2 h5.po.9.8 h8.p2.9.4 h8.p3.9.9 h8.p5.9.4 h8.pa.9.8 ha.po.9.5 ha.pt.9.3 hd.pq.9.2 he.pa.9.7 he.ph.9.4 hf.ps.9.3 hg.p8.9.4 hh.p3.9.8 hh.p7.9.6 hh.pe.9.4 hi.p8.9.5 hk.p4.9.5 hn.p4.9.6 hn.pl.9.b hn.ps.9.6 hr.p1.9.m hr.p6.9.6 hr.pf.9.2 hr.pj.9.8 hs.pf.9.3 hx.pj.9.7 i0.pl.9.e i1.pu.9.6 i3.po.9.5 i4.pp.9.f i5.p7.9.5 fp.2f.a.8 fq.6z.a.4 fr.4b.a.7 fs.h.a.d ft.2r.a.4 fu.2k.a.4 fv.2k.a.5 fw.6s.a.e fx.b.a.4 fy.9.a.6 fz.m.a.3 g0.69.a.4 g1.37.a.8 g2.9.a.6 g3.3o.a.4 g4.x.a.6 g5.x.a.j g6.y.a.5 g7.t.a.4 g8.2k.a.2 g9.x.a.i ga.9.a.4 gb.9.a.4 gc.1m.a.5 gd.4d.a.4 ge.1j.a.4 gf.52.a.5 gg.66.a.4 gh.4d.a.4 gi.5e.a.c gj.3o.a.4 gk.t.a.8 gl.52.a.9 gm.y.a.4 gn.9.a.6 go.1t.a.4 gp.g.a.2 gq.1j.a.5 gr.q.a.2 gs.7s.a.3 gt.k.a.e gu.9.a.6 gv.55.a.c gw.9.a.4 gx.v.a.b gy.5h.a.2 gz.x.a.d h0.7e.a.7",
"h1.71.a.9 h2.1.a.2 h3.1y.a.6 h4.19.a.5 h5.9.a.8 h6.7s.a.2 h7.m.a.5 h8.3o.a.3 h9.4r.a.3 ha.a.a.4 hb.68.a.5 hc.2s.a.6 hd.9.a.3 he.6.a.2 hf.d.a.9 hg.1j.a.4 hh.1n.a.5 hi.5r.a.4 hj.x.a.5 hk.1t.a.6 hl.1x.a.2 hm.41.a.3 hn.2f.a.8 ho.9.a.4 hp.1t.a.2 hq.p.a.6 hr.h.a.8 hs.2s.a.3 ht.4r.a.2 hu.z.a.3 hv.p.a.3 hw.q.a.3 hx.t.a.6 hy.5d.a.8 hz.4q.a.2 i0.7s.a.3 i1.9.a.6 i2.4r.a.4 i3.1m.a.3 i4.10.a.2 i5.9.a.3 i6.11.a.b fp.n8.b.13 fq.nb.b.14 fr.n8.b.2i fs.n8.b.i ft.ng.b.21 fu.ne.b.m fv.n9.b.24 fw.n8.b.1d fx.n8.b.f fy.n8.b.2n fz.n8.b.v g0.n9.b.22 g1.ne.b.e g2.n9.b.19 g3.nc.b.10 g4.n9.b.15 g5.n8.b.h g6.n9.b.2t g7.n9.b.3b g8.n8.b.t g9.n8.b.3 ga.n8.b.14 gb.nb.b.u gc.nk.b.s gd.n8.b.19 ge.n8.b.q gf.n8.b.15 gg.n8.b.1g gh.nd.b.9 gi.n8.b.c gj.nj.b.t gk.n9.b.21 gl.n9.b.3u gm.nc.b.x gn.na.b.2f go.n9.b.n gp.n8.b.18 gq.nc.b.2d",
"gr.n9.b.2c gs.n8.b.1a gt.n9.b.1s gu.nc.b.1c gv.nb.b.1e gw.n9.b.13 gx.nh.b.f gy.n8.b.5 gz.n8.b.d h0.nb.b.f h1.n8.b.s h2.np.b.f h3.n8.b.f h4.n8.b.1h h5.n9.b.1u h6.n8.b.d h7.n8.b.17 h8.nd.b.17 h9.n9.b.1m ha.n8.b.18 hb.nf.b.f hc.n9.b.28 hd.n9.b.1v he.n8.b.2c hf.n8.b.y hg.n9.b.21 hh.n8.b.29 hi.n8.b.g hj.n8.b.1r hk.n8.b.15 hl.nc.b.m hm.n8.b.14 hn.nc.b.1e ho.n8.b.1m hp.n9.b.18 hq.nd.b.c hr.nb.b.1r hs.n8.b.1k ht.n9.b.r hu.nb.b.c hv.ne.b.m hw.n8.b.w hx.n9.b.2m hy.n8.b.2n hz.no.b.k i0.n8.b.1n i1.nc.b.33 i2.nf.b.15 i3.n8.b.k i4.n9.b.1z i5.nb.b.1p i6.nk.b.f p1.1t.c.1 p2.3o.c.1 p3.3o.c.1 p4.b.c.1 p5.b.c.1 p6.9.c.1 p7.3o.c.1 p8.1i.c.1 p9.3o.c.1 pa.26.c.1 pb.6.c.1 pc.6.c.1 pd.6.c.1 pe.26.c.1 pf.9.c.1 pg.42.c.1 ph.6.c.1 pi.1b.c.1 pj.1t.c.1 pl.l.c.1 pm.9.c.1 po.9.c.1 pp.y.c.1 pq.2o.c.1 pr.f.c.1 ps.2f.c.1 pt.2o.c.1 pu.13.c.1",
"p1.o2.d.1 p2.o7.d.1 p2.nr.d.1 p2.ns.d.1 p2.o2.d.1 p2.o3.d.1 p2.nx.d.1 p2.o4.d.1 p2.nt.d.1 p2.ny.d.1 p2.o0.d.1 p2.nq.d.1 p2.oa.d.1 p2.o1.d.1 p2.ob.d.1 p2.nz.d.1 p3.o7.d.1 p3.nu.d.1 p3.nr.d.1 p3.ns.d.1 p3.nv.d.1 p3.o2.d.1 p3.o3.d.1 p3.nw.d.1 p3.nx.d.1 p3.ot.d.1 p3.o4.d.1 p3.nt.d.1 p3.ny.d.1 p3.o0.d.1 p3.nq.d.1 p3.oa.d.1 p3.o1.d.1 p3.ob.d.1 p3.nz.d.1 p4.o8.d.1 p5.o8.d.1 p6.nr.d.1 p6.o2.d.1 p7.o7.d.1 p7.ns.d.1 p7.o2.d.1 p7.o3.d.1 p7.nw.d.1 p7.nx.d.1 p7.ot.d.1 p7.o4.d.1 p7.nt.d.1 p7.ny.d.1 p7.o0.d.1 p7.nq.d.1 p7.oa.d.1 p7.o1.d.1 p7.ob.d.1 p7.nz.d.1 p8.nr.d.1 p9.o7.d.1 p9.nu.d.1 p9.nr.d.1 p9.ns.d.1 p9.nv.d.1 p9.o2.d.1 p9.o3.d.1 p9.nw.d.1 p9.nx.d.1 p9.ot.d.1 p9.o4.d.1 p9.nt.d.1 p9.ny.d.1 p9.o0.d.1 p9.nq.d.1 p9.oa.d.1 p9.o1.d.1 p9.ob.d.1 p9.nz.d.1 pa.o8.d.1 pb.nr.d.1 pc.nr.d.1 pd.nr.d.1 pe.o8.d.1",
"pf.nr.d.1 pf.o2.d.1 pg.o5.d.1 ph.nr.d.1 pi.o3.d.1 pi.ny.d.1 pj.o2.d.1 pk.o5.d.1 pl.or.d.1 pl.nz.d.1 pm.nr.d.1 pm.o2.d.1 pm.nz.d.1 pn.o5.d.1 po.nr.d.1 po.o2.d.1 pp.nt.d.1 pp.nz.d.1 pq.nr.d.1 pr.o5.d.1 ps.nq.d.1 pt.nr.d.1 pu.nr.d.1 8m.4a.e.1.1 8o.5e.e.1.1 8p.43.e.1 8p.41.e.1.1 8p.4s.e.1.1 8q.x.e.1 8q.6p.e.1 8r.6p.e.1 8r.6t.e.1.1 8s.2h.e.1 8t.3l.e.1 8v.3e.e.1 8w.1q.e.1.1 8y.u.e.1 8z.i.e.1 90.2.e.1.1 91.2g.e.1 91.4a.e.1.1 91.79.e.1.1 93.4j.e.1 97.u.e.1 9c.7m.e.1 9c.7r.e.1 9d.1e.e.1 9d.1q.e.1.1 9g.7r.e.1 9h.3s.e.1 9i.1f.e.1.1 9n.2d.e.1.1 9o.7r.e.1 9o.1q.e.1.1 9o.6k.e.1.1 9p.4e.e.1 9p.2d.e.1 9r.1g.e.1"
].join(" ");
const EB0 = [
"9s.u.e.1 9s.6o.e.1 9u.2.e.1 9u.18.e.1 9u.k.e.1 9v.3g.e.1 9y.0.e.1 a2.1n.e.1 a2.7j.e.1 a3.1z.e.1 a4.b.e.1.1 a5.4b.e.1 a5.47.e.1 a6.5t.e.1.1 a7.w.e.1 a8.2.e.1.1 a9.3u.e.1 ab.56.e.1 ad.6i.e.1.1 af.32.e.1 af.52.e.1 af.7y.e.1 aj.1n.e.1 al.i.e.1 ao.5r.e.1.1 ao.4.e.1.1 ao.5e.e.1.1 au.0.e.1 av.0.e.1 ay.34.e.1 ay.6p.e.1 ay.66.e.1.1 az.1j.e.1 b1.n.e.1 b1.3u.e.1 b9.6.e.1 bb.3h.e.1.1 bc.0.e.1 be.6p.e.1 bg.o.e.1 bj.5g.e.1 bk.6t.e.1.1 bk.6p.e.1.1 bm.p.e.1 bn.5e.e.1 bo.1o.e.1.1 bp.j.e.1.1 bu.1f.e.1 bw.2d.e.1 c0.6p.e.1 c2.2o.e.1 c4.1o.e.1 c5.6i.e.1.1 c7.1n.e.1 cb.4s.e.1 cc.55.e.1 ce.4.e.1 ck.1l.e.1 co.11.e.1 cp.7g.e.1 cq.42.e.1 cs.47.e.1 ct.0.e.1.1 ct.1t.e.1.1 cv.1n.e.1 cw.b.e.1 cx.60.e.1 cx.37.e.1 cx.e.e.1 d1.b.e.1 d5.z.e.1.1 de.5x.e.1 df.g.e.1 df.42.e.1 dg.1i.e.1 dj.47.e.1 dk.3.e.1 dk.80.e.1 dk.3y.e.1.1 dv.1p.e.1",
"e1.4k.e.1 ed.f.e.1 eu.x.e.1.1 8w.nu.f.1.1 8x.nr.f.1 8y.nt.f.1 97.nt.f.2 9e.nt.f.2 9i.nz.f.1 9j.or.f.1.1 9j.o0.f.1 9u.ob.f.2 a2.nu.f.2 ac.or.f.1.1 af.nz.f.1 ak.o3.f.1 am.nz.f.2 an.nz.f.2 as.oa.f.1 at.nz.f.1 b5.nv.f.1 b9.nz.f.2 bl.nr.f.1 bv.o2.f.1 bw.nz.f.1 c0.ns.f.2 ck.nt.f.2 cr.o5.f.1 cv.nz.f.2 d6.nt.f.1 dj.nr.f.2 dj.o5.f.1.1 e0.ny.f.1 e4.o2.f.2 eg.o2.f.1.1 8r.nf.g.1 90.n9.g.2 90.n8.g.2 9a.n8.g.1 9j.nn.g.3 a0.ne.g.1 a7.n8.g.1 ae.ni.g.2 aj.n8.g.1 aj.n9.g.1 b7.nf.g.3 bk.nf.g.2 br.n8.g.1 c2.nn.g.2 cz.n9.g.2 df.n8.g.2 e1.n9.g.1 eg.nk.g.8 fo.na.g.2 m4.mw.h.1.1 m4.n2.h.1.1 m4.my.h.1.1 m4.mt.h.1.1 m4.mr.h.1.1 m5.mr.h.1.1 m6.ms.h.1.1 m7.mv.h.1.1 m7.n3.h.1.1 m8.mu.h.1.1 m9.n0.h.1.1 m9.n2.h.1.1 m9.mt.h.1.1 ma.ms.h.1.1 mb.mt.h.1.1 mc.mz.h.1.1 md.mt.h.1.1 me.mt.h.1.1 mf.n1.h.1.1 mg.mx.h.1.1 mh.mr.h.1.1 mi.mr.h.1.1 mj.n6.h.2.1 mk.n6.h.2.1 ml.my.h.1.1 mm.my.h.1.1",
"mn.mw.h.1.1 mo.n4.h.1.1 mp.n7.h.1.1 mq.n0.h.1.1 mr.9s.i.1 mr.9u.i.1 mr.c6.i.1 mr.9l.i.2 mr.9j.i.2 mr.8t.i.1 mr.8o.i.1 mr.cf.i.1 mr.bd.i.3 mr.b1.i.1.1 mr.92.i.1 mr.ak.i.1 mt.9d.i.2 mt.d1.i.1 mt.cw.i.2 mw.cq.i.1 mw.8m.i.1 mw.bp.i.1 my.9a.i.2 my.8k.i.4.1 my.ah.i.1.1 n0.a2.i.2.1 n3.bq.i.1 n5.95.i.1 n5.a4.i.1 n5.da.i.1 n5.9k.i.1.1 n5.ds.i.2 mr.3u.j.7 mr.3.j.7 mr.18.j.7 mr.10.j.7 mr.i.j.7 mr.65.j.7 ms.7u.j.6 ms.6w.j.5 ms.2.j.5 ms.8a.j.5 ms.37.j.5 ms.m.j.5 mt.e.j.7 mt.2t.j.7 mt.4c.j.7 mt.v.j.7 mt.48.j.6 mt.2.j.6 mu.h.j.5 mu.3u.j.3 mu.1p.j.1 mu.2b.j.6.1 mu.22.j.5.1 mu.n.j.5.1 mv.28.j.6 mv.3z.j.5 mv.62.j.5 mv.6a.j.4 mv.5z.j.4 mv.1k.j.4 mw.p.j.8 mw.6e.j.8 mw.4o.j.8 mw.2z.j.8 mw.18.j.7 mw.3c.j.7 mx.3.j.5 mx.2i.j.5 mx.72.j.5 mx.4w.j.5 mx.4s.j.5 mx.1.j.5 my.3u.j.6 my.1d.j.6 my.6s.j.4 my.p.j.4 my.4b.j.4 my.63.j.4",
"mz.4y.j.6 mz.3s.j.6 mz.1k.j.6 mz.k.j.6 mz.62.j.6 mz.7o.j.6 n0.18.j.5 n0.3v.j.5 n0.3i.j.4 n0.3.j.4 n0.16.j.4 n0.4c.j.4 n1.15.j.2 n1.k.j.2 n1.5.j.2 n1.2k.j.2 n1.51.j.2 n1.3k.j.2 n2.6w.j.5 n2.69.j.5 n2.2e.j.4 n2.1j.j.4 n2.4h.j.3 n2.1k.j.3 n3.2j.j.6 n3.5s.j.6 n3.3z.j.6 n3.1d.j.6 n3.62.j.5 n3.48.j.5 n4.3z.j.5 n4.63.j.5 n4.2t.j.5 n4.v.j.4 n4.h.j.4 n4.6p.j.4 n5.28.j.7 n5.4c.j.5 n5.2p.j.5 n5.66.j.5 n5.7.j.4 n5.k.j.4 n6.r.j.3 n6.g.j.2 n6.79.j.2 n6.3f.j.2 n6.2.j.2 n6.10.j.2 n7.3v.j.5 n7.6s.j.4 n7.43.j.4 n7.b.j.4 n7.7n.j.4 n7.q.j.3 mr.53.k.e2y mr.3t.k.chl mr.4h.k.c5i mr.35.k.ayp ms.7c.k.rs mt.7e.k.g7c mt.2t.k.a14 mt.59.k.83o.1 mt.v.k.6r2.1 mu.79.k.4mo mu.1p.k.1jk mu.3f.k.rs mu.2.k.rs mw.4h.k.gs6 mw.l.k.gqs mw.3t.k.fwx mw.s.k.db6 mx.72.k.15o mx.2t.k.dw.1 mx.5o.k.6y mx.1m.k.6y.1 my.2g.k.lzo my.u.k.dqg my.4u.k.b6s my.9.k.8hk n0.16.k.8xa"
].join(" ");
const EB1 = [
"n0.9.k.3h0 n0.1s.k.2jo n0.6u.k.20h n1.w.k.rs.1 n2.1f.k.1ggw n2.1y.k.11i0 n2.u.k.vmw n2.11.k.lke n3.1.k.4tm n3.5h.k.2w6 n3.l.k.2p8 n3.5y.k.2p8 n4.u.k.8rc n4.5.k.3a2 n4.55.k.2p8 n4.13.k.2bc.1 n5.7.k.93s n5.9.k.5za n5.y.k.48s.1 n5.4e.k.48s n6.3.k.15o n6.4b.k.6y n6.45.k.2s n7.4p.k.334.1 n7.4r.k.2bc.1 n7.2g.k.1xg.1 n7.53.k.1xg.1 i9.35.l.nw8b6 i9.4u.l.lycaf i9.5.l.4byum i9.k.l.1si4b i9.6b.l.1eb62 ia.4u.l.4j9oc ib.35.l.7kjrm ib.1a.l.7iab4 ib.4u.l.6p1o2 ib.2m.l.3g139 ic.1k.l.5zc2g ic.r.l.5z6nb ic.2w.l.wrxg ic.1s.l.dk14 ic.3t.l.azb9 id.r.l.1o69t id.3j.l.1gxfn ie.1c.l.690vj ie.4t.l.10y8m if.4v.l.7nor ih.81.l.1c5tx ij.15.l.1p40f ij.54.l.1cvq6 ij.77.l.16los ij.1d.l.158qd ij.19.l.12d5z ik.35.l.mhx in.57.l.1apwe in.39.l.lei3 io.1c.l.a8jox iv.a.l.jbod iw.v.l.1p9tq iw.3a.l.ndmm ix.3.l.w458 ix.4v.l.aef5 ix.k.l.6ajx iz.r.l.1q5jr j0.21.l.6doa5 j1.2w.l.d4jp j1.1w.l.7liz j1.c.l.3kvi j1.2x.l.2jzn i8.4u.m.1an8es i8.35.m.170wqq i8.1a.m.zvbo9 i8.4.m.jhn3y i8.2m.m.dxuf6 ia.6c.m.7u3wy ia.3j.m.7en55 ia.1w.m.6u73s ia.7k.m.3y2vb ib.1w.m.3pw90 id.4u.m.3iebn",
"id.1a.m.16wsy id.14.m.13dei if.r.m.97v8u if.a.m.780va if.5.m.2n5u7 if.t.m.ah3i ig.7k.m.3hja8 ig.85.m.29l1w ig.5l.m.17kvt ig.81.m.15yf5 ig.54.m.uzyd ih.29.m.2gsoc ih.28.m.1gisx ih.y.m.1gc1k ih.1b.m.1g6x6 ii.2m.m.j2gn0 ik.1k.m.6jfm2 ik.a.m.62ssm il.4u.m.8a8oo il.35.m.1wfrz il.3.m.1urpt im.4u.m.5nm6b im.q.m.3jw5a im.7x.m.20cxb im.3.m.go0 im.23.m.7ps in.2c.m.1cu5b in.4u.m.13ipx in.3.m.y5o3 ip.3.m.9krqd iq.1a.m.69g20 iq.2m.m.3azy4 ir.23.m.9fvng is.5o.m.1nm0q is.4k.m.16f35 is.7.m.11q9y is.2i.m.rhbm is.8.m.leka it.c.m.9d3wx iu.q.m.8rqpy iv.4u.m.1hnua iv.35.m.w6qm iv.v.m.ii62 iv.80.m.iatr iw.54.m.3jzyf iw.78.m.15vey iw.5l.m.mjd6 ix.5l.m.h1hv ix.3j.m.9rua iy.59.m.4ks8e iy.q.m.277pf iy.2c.m.itox iz.1b.m.r9v8 iz.4m.m.hjvq iz.3p.m.gxvx iz.2m.m.8w55 j1.6.m.3n1m j2.73.m.8164u j2.o.m.80r5d j2.8.m.4z52z j2.80.m.4ogxt j2.1b.m.4e8hr 8l.j1.n.9n8 8m.j2.n.334 8y.j1.n.2bc 91.j2.n.5sc 96.j1.n.1cm 9g.j1.n.15o 9i.j1.n.15o.1 9k.j1.n.15o 9v.j1.n.1xg 9z.j1.n.bko a5.j2.n.rs a8.j2.n.tx.2 a9.j2.n.2cvk ac.j1.n.15o ag.j1.n.bko b1.j1.n.6y b6.j1.n.2bc b7.j1.n.ku.2",
"bo.j1.n.c2q bt.j1.n.dw ca.j1.n.1xg ci.j1.n.6y cs.j1.n.dw d3.j1.n.1xg fp.jb.o.4618g fp.ja.o.4gr1c fq.j3.o.d5ogw fq.jb.o.39vts fq.ja.o.qsi8 fr.jb.o.g2pc fs.jf.o.x50t fs.j2.o.6fhc fs.in.o.4abk fu.jb.o.7i28 fu.ja.o.37qo fx.ja.o.lfls fz.jb.o.3r14 fz.j2.o.3r14 fz.jd.o.3r14 fz.ja.o.3r14 g0.jb.o.sedk g1.id.o.13pinl g1.jj.o.rzo0 g2.jd.o.bsds g3.j2.o.4abk g4.j9.o.48lsq g5.ji.o.255s g5.in.o.12kw g9.j2.o.1hmz7 g9.jd.o.16v7k g9.je.o.16v7k g9.ji.o.nkrk g9.in.o.12kw ga.ja.o.5fkw8 ga.jb.o.5ads4 ga.j8.o.lfls ga.jc.o.5cwg ga.ix.o.uv4 gc.ja.o.255s gg.j4.o.9m6g2 gg.jg.o.tgyg gi.in.o.2og8 gk.jb.o.lfls go.j2.o.hd0 gp.ij.o.1jo123 gp.i9.o.1hl0g gp.ic.o.1hl0g gp.jk.o.lfls gp.j2.o.w5eo gp.ja.o.w5eo gp.jd.o.w5eo gp.jb.o.lfls gv.ja.o.9n80 gx.ie.o.oersw gz.jh.o.rv34 h6.j6.o.5ycte h8.j8.o.lfls h9.j7.o.5yc1s h9.j8.o.4rgu8 h9.jb.o.3iggw h9.ja.o.3vik6 h9.jc.o.2dqf4 hi.j5.o.ctp2h ho.iv.o.h6cly hp.j8.o.lfls ht.j8.o.lfls ht.jb.o.37qo ht.ja.o.12kw fp.jb.p.4618g fp.ja.p.4gr1c fq.j3.p.d5ogw fq.jb.p.39vts fq.ja.p.qsi8 fr.jb.p.g2pc fu.jb.p.7i28 fx.ja.p.lfls g1.id.p.13pinl g1.jj.p.rzm7",
"g2.jd.p.bsds g4.j9.p.48lsq g9.j2.p.1hmz7 g9.jd.p.16v7k g9.je.p.16v7k g9.ji.p.nkrk gg.j4.p.9m52h gg.jg.p.tgyg gk.jb.p.lfls gv.ja.p.9n80 gx.ie.p.oersw gz.jh.p.rv34 h6.j6.p.5ycte hi.j5.p.ctnvy ho.iv.p.h6cly hp.j8.p.lfls k9.jk.p.4f0rzn kc.jl.p.1thojk ke.j2.p.2btkr3 kf.is.p.5n2sh kf.jk.p.1satc kf.j2.p.13ngw kf.jd.p.qsi8 kg.ib.p.ujjc0 kh.jp.p.4ki2g kh.jk.p.4618g kh.j2.p.16v7k kh.id.p.15smo kj.ja.p.1rat1c kk.jb.p.1rvu6m kl.in.p.rvu0b ks.jn.p.e2oqo ks.jq.p.3s3ow ku.jp.p.apsw kv.jo.p.66par kw.jm.p.s3lps kx.is.p.42ths kx.ja.p.2z60w kx.jc.p.lfls kx.j7.p.lfls ky.iz.p.1satc ky.is.p.b93c g1.k9.q.2dqf4 g1.kh.q.17ei0 g1.l1.q.lfls0 k9.kf.q.xuhqo k9.kd.q.45qin4 k9.l2.q.kct68 k9.la.q.bgle8 k9.lb.q.9z0ds k9.ld.q.94czk k9.li.q.83g3a kc.ko.q.572e9s ke.kh.q.lm19c ke.l0.q.mx6sg kf.kh.q.x5ue8 kf.g1.q.70tuo kf.kx.q.41qww kf.kv.q.lfls kf.ho.q.lfls kf.lf.q.8c2gw kg.km.q.201g74 kg.l9.q.dkolc kh.g1.q.3qte8 kh.kl.q.3klmo kh.ky.q.25dhs kh.ke.q.1satc kh.kf.q.lfls kh.lg.q.8aw14 kk.l4.q.gjf6o kl.l5.q.ft240 kl.l7.q.dzops kn.l3.q.j2l2v kn.l8.q.ds63f ko.kh.q.5cwg0 ko.fw.q.3b64g ko.k9.q.1satc ko.kf.q.230m8 ko.kx.q.lfls ko.lc.q.9qqt1"
].join(" ");
const EB2 = [
"kt.le.q.8i6dk ku.k9.q.3vbfk ku.kh.q.16v7k ku.kf.q.lfls kv.k9.q.tro8w kx.kf.q.35etg kx.ky.q.ztq4 fq.lh.r.83pqi g1.id.r.lfls0 gx.ie.r.evu4g k9.jk.r.45qin4 ke.j2.r.mx6sg kg.ib.r.dkolc kj.ja.r.yrpq8 kk.l4.r.gjf6o kl.in.r.ft240 ks.jn.r.e2kvs kv.jo.r.62mdc kz.l6.r.e8tft ft.ka.s.egu0 ft.kb.s.b9v4 fv.ka.s.g6k8 fv.ki.s.boiw fy.ka.s.12x8g fy.kb.s.lyw8 fz.kb.s.u26c fz.kq.s.giwo fz.kp.s.aqyk g0.kb.s.e1eg g3.ka.s.avl8 g6.kb.s.1j6vs g6.ka.s.1j6vs g6.ki.s.i22s g6.kp.s.bsqu g6.kq.s.bsds g7.ka.s.lnbk g7.kb.s.eewk ga.kp.s.1gifk ga.kb.s.1frfc ga.ki.s.1f4xf ga.ka.s.yspa ga.kr.s.nshc ga.kq.s.ji5s gd.ka.s.cn8w ge.ka.s.boiw gf.ka.s.b93c gf.ki.s.b93c gp.ka.s.ew9k gp.kp.s.b58g gr.kb.s.23jwo gr.ka.s.1jaqo gr.ki.s.c3yg h9.kb.s.1fjpk h9.ki.s.qsi8 h9.kr.s.nkrk h9.ka.s.jg8c hg.ka.s.f3zc hh.ka.s.sk5w hh.kb.s.hud0 8u.m2.t.1 90.m1.t.1 a8.m3.t.1 cy.fr.t.1 dh.lv.t.1 du.lw.t.1 e8.ly.t.1 ea.lu.t.1 ec.ls.t.1 eh.ly.t.1 ej.lx.t.1 ev.lz.t.1 f0.m0.t.1 f1.g1.t.1 fe.lt.t.1 fz.gf.u.1 g0.ge.u.1 g7.hs.u.1 ge.hs.u.1 gn.g7.u.1 gn.gd.u.1",
"gw.hg.u.1 hw.i4.u.1 hx.gn.u.1 hx.gj.u.1 hx.hk.u.1 i1.hk.u.1 i1.gj.u.1 0.oz.v.1 1.nv.v.1 2.o6.v.1 4.o5.v.1 7.ny.v.1 9.nr.v.1 b.o8.v.1 b.oi.v.1 b.oy.v.1 f.oo.v.1 h.of.v.1 l.ow.v.1 l.nz.v.1 m.oc.v.1 n.oi.v.1 p.p0.v.1 w.oi.v.1 x.om.v.1 11.oj.v.1 12.nt.v.1 19.ov.v.1 19.ox.v.1 19.ot.v.1 1j.on.v.1 1l.nt.v.1 1n.oi.v.1 1o.oe.v.1 1p.os.v.1 1t.o2.v.1 1y.oq.v.1 22.o6.v.1 26.o8.v.1 26.oi.v.1 29.ol.v.1 2b.nr.v.1 2d.o9.v.1 2d.ow.v.1 2f.nq.v.1 2h.om.v.1 2l.o9.v.1 2l.ow.v.1 2n.o4.v.1 2t.og.v.1 2v.or.v.1 2x.nu.v.1 2z.ou.v.1 34.ot.v.1 37.oj.v.1 38.og.v.1 3d.ou.v.1 3g.o5.v.1 3h.o1.v.1 3l.os.v.1 3o.ns.v.1 3q.ob.v.1 3u.nw.v.1 3w.ot.v.1 3x.ol.v.1 3y.oo.v.1 3y.oz.v.1 3y.oy.v.1 3z.nw.v.1 41.ny.v.1 42.op.v.1 42.ov.v.1 42.ox.v.1 44.ol.v.1 46.nr.v.1 4b.ok.v.1 4j.nz.v.1 4x.p0.v.1 52.oe.v.1 56.ns.v.1",
"58.op.v.1 58.ov.v.1 58.ox.v.1 5e.oh.v.1 5f.o3.v.1 5g.nq.v.1 5r.on.v.1 5t.nt.v.1 5y.nu.v.1 61.o0.v.1 65.o4.v.1 69.oh.v.1 6i.oq.v.1 6m.od.v.1 6o.nu.v.1 6p.oi.v.1 75.nx.v.1 7f.o2.v.1 7s.o3.v.1 82.oa.v.1 0.1y.w.r 0.2.w.1o 2.0.w.1a 3.3d.w.1l 4.38.w.1g 4.5z.w.q 8.1s.w.14 8.1e.w.11 8.5q.w.11 8.4y.w.x 8.1w.w.u 8.5j.w.t 8.47.w.o a.5i.w.1h f.52.w.p h.p.w.p n.10.w.1c o.6w.w.r p.0.w.v v.1s.w.1r v.2n.w.1d x.6s.w.1l x.5r.w.1h z.p.w.10 1p.2.w.1k 1s.v.w.22 1s.8.w.18 1s.28.w.w 1s.50.w.s 1s.2n.w.p 1y.0.w.p 25.69.w.r 25.0.w.q 28.1s.w.1c 2d.4b.w.2j 2d.x.w.27 2e.58.w.1q 2j.1s.w.p 2l.2t.w.24 2u.8.w.w 2z.6e.w.1j 36.2.w.1h 38.4.w.q 3d.3.w.1f 3r.0.w.t 3v.5r.w.1o 3y.5r.w.1i 3y.x.w.1c 42.6p.w.r 43.i.w.23 44.69.w.1a 44.0.w.u 4b.x.w.2z 4b.2d.w.1o 4b.3y.w.1e 4o.5e.w.2b 4o.6e.w.1k 4x.1y.w.12 52.69.w.17 52.x.w.1a",
"54.3p.w.z 54.4m.w.p 54.v.w.o 58.6s.w.26 58.x.w.21 58.6e.w.1u 58.4b.w.1j 5e.69.w.y 5e.6s.w.1k 5i.69.w.s 5j.8.w.x 5q.8.w.o 5r.x.w.2s 5r.5e.w.2c 5r.6s.w.1s 5r.4b.w.1r 5r.3y.w.1e 5r.52.w.1c 5z.38.w.1a 5z.52.w.w 5z.5e.w.u 5z.4b.w.r 5z.4.w.q 63.x.w.1s 63.4b.w.1p 63.6s.w.1l 67.69.w.x 69.5e.w.w 6e.5r.w.1j 6e.2z.w.1i 6e.x.w.1e 6e.5e.w.1c 6s.x.w.2h 6s.4b.w.1p 6s.5e.w.1k 6s.6e.w.1k 6s.5r.w.1h 6s.58.w.1g 6w.o.w.q 7f.8.w.o 9q.nv.x.1.2 ap.nw.x.1.2 cy.nq.x.1 cy.nt.x.1 ey.o6.x.1.2 f2.ot.x.1.2 f2.ob.x.1.2 f5.of.x.1.2 f7.ns.x.2.2 fp.nq.y.1.1 fq.nv.y.1.1 fr.nt.y.2.1 fs.nz.y.1.1 ft.nt.y.1.1 fu.nt.y.2.1 fv.nx.y.1.1 fw.o0.y.3.1 fx.nq.y.4.1 fy.o4.y.2.1 fz.nz.y.1.1 g0.nx.y.1.1 g2.o4.y.2.1 g4.of.y.1.1 g5.nx.y.1.1 g6.nz.y.1.1 gb.o4.y.2.1 gd.nt.y.2.1 ge.oq.y.1.1 gf.oi.y.1.1 gg.o3.y.2.1 gj.oq.y.1.1 gk.nx.y.2.1 gl.nt.y.1.1 gn.o1.y.1.1 gp.nu.y.1.1 gs.ob.y.1.1 gt.nx.y.1.1 gu.o6.y.4.1 gv.oe.y.1.1 gy.o2.y.1.1"
].join(" ");
const EB3 = [
"gz.oq.y.1.1 h0.nt.y.1.1 h1.oj.y.2.1 h2.nv.y.1.1 h3.o4.y.2.1 h4.nv.y.5.1 h5.nz.y.1.1 h6.oo.y.2.1 h7.nq.y.2.1 h8.o6.y.1.1 ha.oa.y.2.1 hb.nu.y.2.1 hc.ob.y.1.1 hf.nq.y.2.1 hj.nq.y.1.1 hl.nt.y.3.1 hm.oo.y.1.1 hq.o0.y.1.1 hr.o3.y.2.1 hs.nz.y.1.1 hy.nx.y.1.1 i0.o3.y.3.1 i1.oq.y.1.1 i2.nu.y.3.1 i3.nx.y.1.1 i4.of.y.1.1 i6.ny.y.2.1 i7.nt.y.1.1 1.pw.z.1.1 4.q2.z.1.1 5.pw.z.1.1 5.px.z.1.1 6.pz.z.1.1 6.px.z.1.1 7.pw.z.1.1 7.pz.z.1.1 8.px.z.1.1 8.q2.z.1.1 9.pw.z.1.1 9.px.z.1.1 a.q0.z.1.1 a.q2.z.1.1 c.pv.z.1.1 c.q2.z.1.1 e.px.z.1.1 e.q2.z.1.1 k.px.z.1.1 l.pw.z.1.1 l.pz.z.1.1 m.py.z.1.1 o.pz.z.1.1 o.q2.z.1.1 p.q2.z.1.1 r.q1.z.1.1 s.pw.z.1.1 s.pz.z.1.1 s.px.z.1.1 t.pw.z.1.1 t.pz.z.1.1 u.pw.z.1.1 u.pz.z.1.1 v.px.z.1.1 v.q2.z.1.1 w.px.z.1.1 y.px.z.1.1 y.q2.z.1.1 12.pw.z.1.1 12.q2.z.1.1 14.pw.z.1.1 15.py.z.2.1 15.q0.z.1.1 15.pv.z.1.1 15.q1.z.1.1 16.pz.z.1.1 1b.pz.z.1.1 1c.q0.z.1.1 1c.pv.z.1.1 1e.q0.z.1.1 1e.pv.z.1.1 1e.q1.z.1.1",
"1f.pz.z.1.1 1l.pv.z.1.1 1l.q1.z.1.1 1q.q0.z.1.1 1q.pv.z.1.1 1s.q0.z.1.1 1s.pv.z.1.1 1u.py.z.2.1 1u.pv.z.1.1 27.q0.z.1.1 2g.py.z.2.1 2g.q1.z.1.1 2u.q0.z.1.1 2w.py.z.2.1 2w.q1.z.1.1 2x.q1.z.1.1 2y.pv.z.1.1 2z.q0.z.1.1 31.py.z.1.1 31.q1.z.1.1 34.pv.z.1.1 34.q1.z.1.1 39.q0.z.1.1 3h.q1.z.1.1 fp.ne.10.15 fq.ne.10.3 fr.ne.10.14 fs.nl.10.8 ft.ne.10.g fu.ne.10.u fv.n9.10.8 fw.n9.10.2 fx.n8.10.1 fy.nd.10.1 fz.nc.10.4 g0.n9.10.1 g1.ne.10.a g2.ne.10.2 g3.ne.10.1 g4.nl.10.2 g5.n9.10.2 g6.nl.10.1 g7.n9.10.2 g8.ne.10.4 g9.ne.10.1 ga.n9.10.2 gb.n8.10.2 gc.ne.10.8 gd.ne.10.7 ge.nc.10.2 gh.nk.10.3 gi.nm.10.1 gj.ne.10.5 gk.n9.10.1 gl.n9.10.2 gm.ne.10.2 gn.nc.10.3 go.n9.10.5 gq.nc.10.2 gr.n9.10.1 gt.nm.10.1 gu.nc.10.6 gw.n9.10.5 gy.n9.10.3 h0.ne.10.6 h1.ne.10.s h3.ne.10.j h4.ne.10.b h5.n9.10.c h7.nl.10.1 h9.n9.10.1 ha.ne.10.8 hb.ne.10.i hc.n9.10.1 hd.n9.10.2 he.ne.10.3 hf.ne.10.5 hg.n9.10.2 hj.nl.10.7 hk.ne.10.e",
"hl.nc.10.a hm.ne.10.f hn.nh.10.2 hp.n9.10.2 hr.nl.10.3 ht.n9.10.2 hv.nk.10.5 hw.n9.10.1 hx.n9.10.3 hy.nl.10.e i0.nl.10.4 i1.nc.10.3 i2.nf.10.3 i3.ne.10.9 i4.n9.10.2 i5.ne.10.3 i6.ne.10.6 i7.nb.10.1 8p.ne.11.2 8p.nb.11.1 8u.n9.11.1.2 8w.nf.11.1 90.n9.11.3 9e.n9.11.1 9r.n9.11.2.2 ab.ne.11.1 ah.nm.11.1.2 aj.n9.11.2 ap.n9.11.1.2 aw.n9.11.2 b3.n9.11.1 b8.nl.11.1 bf.n9.11.1.2 bo.ne.11.1.2 br.n9.11.1 bt.n9.11.1.2 bt.nl.11.1 c7.ne.11.3 c7.nc.11.3 c7.ng.11.1 c7.nd.11.1 dp.nl.11.1 e7.ne.11.2 ei.n9.11.1.2 ey.nc.11.2 ff.nm.11.1 fj.nn.11.1.2 8k.n8.12.2.2 8t.n8.12.4.2 8w.n8.12.3.2 90.n8.12.4.2 95.n8.12.1.2 9c.n8.12.4.2 9d.n8.12.1.2 9l.n8.12.1.2 9s.n8.12.2.2 9u.n8.12.3.2 a5.n8.12.6.2 ae.n8.12.9.2 af.n8.12.2.2 ag.n8.12.1.2 ak.n8.12.1.2 ar.n8.12.1.2 at.n8.12.1.2 ax.n8.12.3.2 az.n8.12.1.2 b1.n8.12.1.2 b3.n8.12.1.2 b6.n8.12.1.2 b7.n8.12.1.2 b8.n8.12.1.2 be.n8.12.2.2 bk.n8.12.3.2 bs.n8.12.1.2 bv.n8.12.3.2 bz.n8.12.1.2 c6.n8.12.3.2 ck.n8.12.1.2 cl.n8.12.1.2 cs.n8.12.2.2",
"cz.n8.12.1.2 d1.n8.12.1.2 d3.n8.12.1.2 db.n8.12.1.2 dc.n8.12.7.2 ds.n8.12.5.2 e4.n8.12.8.2 e7.n8.12.2.2 e8.n8.12.1.2 eb.n8.12.1.2 ed.n8.12.2.2 ef.n8.12.3.2 ek.n8.12.1.2 ey.n8.12.b.2 fb.n8.12.2.2 fc.n8.12.2.2 fd.n8.12.1.2 fp.nb.13.1 fr.nb.13.1 fs.n9.13.1 fu.nb.13.1 fv.n9.13.9 g0.n9.13.5 g2.n9.13.2 g4.n9.13.2 g6.n9.13.1 g7.n9.13.5 gi.n9.13.1 gl.n9.13.5 gm.nb.13.2 go.n9.13.c gp.nb.13.1 gq.nc.13.1 gr.n9.13.3 gt.n9.13.1 gu.nc.13.1 gw.n9.13.6 gy.n9.13.2 h4.n9.13.2 h5.n9.13.d h7.nc.13.1 ha.nb.13.1 hc.n9.13.4 hg.n9.13.1 hl.nc.13.2 hm.nb.13.1 hp.n9.13.1 hr.n9.13.1 hs.n9.13.6 hu.nb.13.1 hx.n9.13.7 i2.nc.13.1 i3.nc.13.2 i4.n9.13.4 i7.n9.13.1 1.gj.14.2 1.hh.14.1 3.fy.14.3 3.hz.14.3 7.fy.14.2 7.g6.14.1 e.fy.14.4 e.h8.14.3 f.fy.14.m f.gf.14.4 s.gs.14.p s.fv.14.9 1j.fy.14.2 1j.gf.14.2 1o.fy.14.a 1o.gf.14.8 1r.fy.14.3 1r.hu.14.3 1s.fy.14.34 1s.h8.14.k 1v.gn.14.1 1y.gj.14.1 1y.hh.14.1 20.fy.14.3 20.hh.14.2"
].join(" ");
const EB4 = [
"21.gf.14.5 21.hh.14.3 23.fv.14.1 2d.gf.14.1 2j.fv.14.b 2p.gn.14.2 2u.gn.14.1 2v.hh.14.2 2w.gs.14.2 2w.gf.14.2 30.g7.14.2 30.hh.14.2 32.gj.14.1 3f.gn.14.3 3f.gf.14.3 3h.hu.14.2 3h.ft.14.1 3i.h8.14.7 3i.gf.14.7 3y.hx.14.4 3y.i4.14.3 3z.hh.14.2 41.gs.14.2 41.gf.14.2 42.h2.14.f 48.h8.14.2 48.hh.14.2 4d.i1.14.1 4g.fy.14.4 4q.i5.14.2 4q.hs.14.2 5f.gn.14.1 5g.gw.14.2 5g.g6.14.2 5h.hh.14.1 5h.gf.14.1 5q.gf.14.1 5t.ft.14.2 5u.fy.14.2 5u.h8.14.2 5w.gf.14.3 5z.fy.14.2 5z.gf.14.2 64.gs.14.1 6c.ft.14.7 6c.gj.14.4 6d.fv.14.4 6d.hx.14.3 6g.gj.14.f 6g.fy.14.e 72.fy.14.6 72.hh.14.2 75.gs.14.3 75.hh.14.2 7v.hh.14.1 7w.hn.14.1 7y.gs.14.f 7y.fv.14.f 82.gf.14.1 8e.hh.14.e 8e.gs.14.b 8h.h8.14.a 8h.gs.14.6 8i.fy.14.2 8i.gf.14.1 8j.gf.14.5 1.gj.15.37qo 5.g7.15.n5c 7.g6.15.12kw 9.gd.15.3uw m.gn.15.7i28 s.hk.15.255s t.hu.15.1e5k 1e.hu.15.12kw 1s.gs.15.33vs 1v.gn.15.37qo 20.hh.15.n5c 21.hh.15.1aao 2a.hu.15.n5c 2g.hu.15.yq0",
"2j.hv.15.4abk 2n.hh.15.1jk 2o.hh.15.bko 2p.h8.15.1e5k 2t.hz.15.0 2u.h8.15.n5c 2v.gd.15.n5c 2w.gs.15.bko 30.fv.15.12kw 3b.hu.15.bq8 3e.hz.15.1e5k 3f.hu.15.12kw 3i.gs.15.bko 3q.hh.15.n5c 3v.hz.15.0 3w.gn.15.255s 46.hu.15.n5c 48.h8.15.0 4f.hh.15.26pc 4h.fy.15.25xk 4t.hu.15.4380 4y.h2.15.1jk 50.hu.15.255s 55.hz.15.0 56.g0.15.bko 5a.hv.15.n5c 5f.gn.15.12kw 5g.hx.15.n5c 5h.gs.15.255s 5i.hz.15.0 5m.h2.15.n5c 5q.g7.15.255s 5t.fv.15.0 5w.gf.15.bko 5x.fy.15.36yw 64.gs.15.12kw 6c.fy.15.591k 6d.gs.15.4abk 6h.hu.15.n5c 6t.hu.15.1e5k 6w.hu.15.n5c 70.hu.15.2gw0 71.hh.15.1pq8 72.fy.15.2hns 75.hh.15.yq0 7c.hu.15.37qo 7e.gf.15.n5c 7f.h2.15.255s 7s.hu.15.n5c 7t.fy.15.n5c 7w.hh.15.2sb4 7y.gs.15.0 7z.gj.15.n5c 82.gf.15.n5c 84.gf.15.255s 85.h2.15.bko 87.hz.15.n5c 89.gf.15.25bc 8e.hh.15.255s 8h.hx.15.12kw 8j.gf.15.12kw fy.75.16.3 fy.3i.16.2 fy.2n.16.2 fy.3u.16.1 fy.1l.16.1 gb.12.16.1 go.7p.16.2 go.t.16.1 go.1u.16.1 go.3k.16.1 go.2a.16.1 i7.61.16.k i7.1q.16.9 i7.68.16.9 i7.4p.16.7 i7.12.16.7 lj.1f.16.2k lj.u.16.2i lj.16.16.1k",
"lj.3i.16.q lj.3s.16.p lk.2n.16.d lk.o.16.c lk.76.16.9 lk.1.16.9 lk.1r.16.8 ll.61.16.f ll.4r.16.b ll.87.16.8 ll.6q.16.4 ll.1r.16.4 lm.3t.16.8 lm.16.16.7 lm.7r.16.6 lm.1f.16.5 lm.64.16.5 ln.75.16.d ln.2g.16.8 ln.4h.16.6 ln.1f.16.5 ln.2y.16.5 lo.12.16.6 lo.27.16.4 lo.6m.16.4 lo.3i.16.3 lo.51.16.3 lp.2y.16.6 lp.3h.16.4 lp.4g.16.3 lp.5u.16.3 lp.73.16.3 lq.14.16.8 lq.v.16.6 lq.7j.16.5 lq.6z.16.5 lq.28.16.4 lr.7t.16.5 lr.1e.16.4 lr.6v.16.4 lr.1m.16.3 lr.4i.16.3 6.13.17.d 6.1v.17.b 9.2r.17.c 9.1v.17.b 9.13.17.b 9.6l.17.7 v.65.17.8 12.2i.17.b 1e.41.17.8 1e.l.17.7 1v.13.17.f 21.6c.17.8 21.1e.17.8 21.41.17.8 2n.7i.17.8 2n.21.17.8 2n.6c.17.8 2n.1e.17.8 2n.41.17.8 30.l.17.9 3k.2i.17.7 3u.65.17.b 4a.13.17.7 4e.5f.17.7 4z.5t.17.c 4z.7y.17.b 4z.40.17.a 4z.5s.17.8 4z.1g.17.7 50.2s.17.9 50.l.17.8 5t.2i.17.e 5t.12.17.b 5t.5s.17.9 5t.66.17.9 5t.65.17.8 5t.8.17.6 66.2i.17.8",
"6c.1e.17.8 6c.41.17.8 7f.5t.17.c 7f.2i.17.b 7f.66.17.9 7f.12.17.8 7i.21.17.8 7i.6c.17.8 7i.1e.17.8 7i.41.17.8 7v.9.17.h 7v.6l.17.8 8k.7n.18.4 ba.35.18.4 ba.16.18.4 ba.52.18.4 ci.85.18.4 cr.5b.18.c ct.7s.18.c cu.5b.18.6 cx.8f.18.c cy.2q.18.c d0.61.18.2 d0.87.18.2 d0.6q.18.4 d2.2x.18.c d3.8g.18.4 d4.m.18.4 d8.89.18.a d8.83.18.6 d9.7z.18.4 da.6v.18.4 da.8i.18.c dc.5x.18.o dd.3s.18.1 de.5x.18.8 df.g.18.4 dg.4a.18.c dh.2q.18.c dj.47.18.8 dk.80.18.8 dl.4a.18.c dm.86.18.o dn.5x.18.c do.j.18.g do.0.18.4 do.2h.18.c do.7x.18.1 dp.34.18.4 dq.7v.18.4 dr.82.18.c ds.3w.18.c dt.53.18.6 dv.1p.18.4 dx.1j.18.2 dy.7y.18.c dz.1i.18.c e0.8i.18.6 e1.4k.18.4 e2.8.18.c e3.86.18.c e4.4a.18.c e5.5x.18.c e6.7w.18.2 e7.8e.18.c e8.4a.18.o e9.8j.18.c ea.2q.18.c eb.52.18.4 ec.62.18.4 ec.4v.18.4 ed.5x.18.4 ee.3q.18.4 ee.6a.18.4 ef.8b.18.2 eg.4a.18.c eh.4a.18.c ei.v.18.c ej.5n.18.8 ej.24.18.g",
"ej.8h.18.c ej.81.18.4 ek.3m.18.c el.5b.18.c em.28.18.8 en.5x.18.o eo.1m.18.c ep.8g.18.c eq.4a.18.o er.7t.18.4 es.7h.18.c et.4f.18.c eu.5.18.4 ev.8d.18.c ew.2j.18.c ex.33.18.c ey.3q.18.c ez.2l.18.4 ez.2t.18.4 f0.4y.18.4 f1.5n.18.4 f2.8.18.o f3.8c.18.2 f3.4y.18.2 f4.8a.18.c f5.4a.18.c f6.4f.18.o f7.g.18.4 f8.4a.18.c f9.84.18.c fa.0.18.4 fb.34.18.c fc.4a.18.c fd.3q.18.4 fd.6x.18.4 fe.4f.18.c ff.4a.18.c fg.y.18.c fh.43.18.4 fi.5x.18.c fj.86.18.c fk.88.18.o fl.7u.18.e fm.28.18.c fn.1b.18.c fo.a.18.c 8n.1n.19.1 8n.i.19.1 8n.w.19.1 8n.35.19.1 8n.f.19.1 8n.4x.19.1 8n.61.19.1 8n.16.19.1 8n.3i.19.1 8n.4i.19.1 8n.1r.19.1 8n.7v.19.1"
].join(" ");
const ESA = [EA0, EA1, EA2, EA3, EA4].join(" ");
const ESB = [EB0, EB1, EB2, EB3, EB4].join(" ");

type Nd = { i: number; k: string; name: string; p: string; sub: string; x: number; y: number; sc: number; m: number[]; d: boolean };
type Ed = { s: number; t: number; ty: number; v: number; c: number };
type View = { x: number; y: number; w: number; h: number };
type Theme = ReturnType<typeof useGrokTheme>;
const RS = [RSA, RSB, RSC, RSD].join("\n").split("\n").filter((s: string) => s.length > 0);
const NODES: Nd[] = RS.map((s: string, i: number) => { const a = s.split("|"); return { i, k: a[0], name: a[1], p: a[2], sub: a[3], x: a[4] ? parseInt(a[4], 36) : 0, y: a[5] ? parseInt(a[5], 36) : 0, sc: a[6] ? parseInt(a[6], 36) / 10 : 0, m: a[7] ? a[7].split(".").map((v: string) => parseInt(v, 36)) : [], d: a[4] !== "" }; });
const EDGES: Ed[] = [ESA, ESB].join(" ").split(" ").filter((t: string) => t.length > 0).map((t: string) => { const a = t.split("."); return { s: parseInt(a[0], 36), t: parseInt(a[1], 36), ty: parseInt(a[2], 36), v: parseInt(a[3], 36), c: a[4] ? Number(a[4]) : 0 }; }).filter((e: Ed) => e.s < NODES.length && e.t < NODES.length);
const mv = (n: Nd, j: number): number => n.m[j] || 0;
const FULL: View = { x: 0, y: 0, w: 1000, h: 700 };
const FAM = ["Money", "Lobbying", "Revolving door", "Foreign", "Outside & dark money", "Legislative", "Executive", "Ethics & travel", "Social"];
const TY: string[][] = ["Direct contributions|0|$", "PAC indirect (pro rata)|0|$", "JFC transfers (pro rata)|0|$", "Lobbyist → PAC or committee|0|$", "Committee → member|0|$", "PAC officer|0|", "Form 3L bundling|0|$", "Bundler's lobbyist|0|", "Lobbies for client (LD-2 $ share)|1|$", "Client lobbied bill|1|filings", "Client lobbied member's bills|1|bills", "Client lobbied agency|1|reports", "Bill sponsor|1|", "Bill referred to committee|1|", "Former personal staff|2|", "Former committee staff|2|", "Former agency official|2|", "Foreign principal → registrant|3|", "FARA agent of registrant|3|", "FARA contact or mention|3|mentions", "FARA-reported contribution|3|$", "IE supporting|4|$", "IE opposing|4|$", "Lobbyist → super PAC|4|$", "Client org → super PAC|4|$", "Nonprofit → super PAC|4|$", "990 grant|4|$", "990 Schedule C political|4|$", "527 → committee|4|$", "990 officer or director|4|", "Board interlock|4|shared directors", "Committee chair or ranking|5|", "Cosponsorship|5|bills", "Hearing witness|5|", "Org testified to committee|5|appearances", "Caucus member|5|", "OIRA meetings (org)|6|meetings", "OIRA meeting attendee|6|meetings", "WH visitor name match|6|visits", "Regulations.gov comments|6|comments", "Stock trades|7|transactions", "Holding (upper bound)|7|$", "Sponsored travel|7|trips", "CODEL together|7|trips", "X interaction|8|w", "Instagram tag|8|"].map((s: string) => s.split("|"));
const TFAM = TY.map((t: string[]) => Number(t[1]));
const LEAN: Record<string, string> = { R: "Republican", D: "Democrat", I: "Independent", M: "Mixed", U: "Unknown" };
const KIND: Record<string, string> = { L: "Lobbyist", M: "Member", K: "Client or company", S: "Super PAC or IE spender", C: "PAC or party committee", N: "Nonprofit, 527 or sponsor", F: "Foreign principal", R: "FARA registrant", A: "Agency", H: "Congressional committee", W: "Bill", U: "Caucus", B: "Bundler" };
const KORD = "MLKSCNFRAHWUB";
const CONF = ["High", "Medium", "Low"];
const usd = (v: number): string => "$" + Math.round(v).toLocaleString("en-US");
const usdM = (v: number): string => "$" + (v / 1e6).toFixed(2) + "M";
const fmtV = (e: Ed): string => { const u = TY[e.ty][2]; return u === "$" ? usd(e.v) : u === "w" ? `weight ${e.v / 4}` : u ? `${e.v.toLocaleString("en-US")} ${u}` : ""; };
const LOBS = NODES.filter((n: Nd) => n.k === "L");
const MEMS = NODES.filter((n: Nd) => n.k === "M");
const CLIS = NODES.filter((n: Nd) => n.k === "K");
const memLob = (n: Nd): number => (mv(n, 1) + mv(n, 2) + mv(n, 3)) * 100;
const nodeScore = (n: Nd, by: string): number => n.k === "L" ? (by === "money" ? mv(n, 1) / 10 : n.sc) : n.sc;

function radius(n: Nd, by: string): number {
  if (n.k === "L" || n.k === "M" || n.k === "K") return 1.6 + 9 * Math.pow(Math.max(0, Math.min(1, (nodeScore(n, by) - 35) / 55)), 2);
  if (n.k === "S") return 2 + 7 * Math.sqrt(Math.min(1, mv(n, 0) / 294000));
  if (n.k === "F" || n.k === "R") return 2 + 6 * Math.sqrt(Math.min(1, mv(n, 0) / 520));
  return 3.2;
}

function NetworkSvg(props: { view: View; setView: (v: View) => void; edges: Ed[]; shown: number[]; sel: number | null; nbrs: Set<number>; onSelect: (i: number | null) => void; ncol: (n: Nd) => string; fcol: (f: number) => string; by: string; theme: Theme }) {
  const { view, setView, edges, shown, sel, nbrs, onSelect, ncol, fcol, by, theme } = props;
  const ref = useRef<SVGSVGElement>(null);
  const viewRef = useRef<View>(view);
  viewRef.current = view;
  const drag = useRef<{ x: number; y: number; vx: number; vy: number; moved: boolean } | null>(null);
  const moved = useRef<boolean>(false);
  useEffect(() => {
    const el = ref.current;
    if (!el) return;
    const h = (e: WheelEvent) => {
      if (!e.ctrlKey && !e.metaKey) return;
      e.preventDefault();
      const rect = el.getBoundingClientRect();
      const fx = (e.clientX - rect.left) / rect.width;
      const fy = (e.clientY - rect.top) / rect.height;
      const v = viewRef.current;
      const w = Math.min(1400, Math.max(60, v.w * (e.deltaY > 0 ? 1.15 : 1 / 1.15)));
      setView({ x: v.x + fx * (v.w - w), y: v.y + fy * (v.h - w * 0.7), w, h: w * 0.7 });
    };
    el.addEventListener("wheel", h, { passive: false });
    return () => el.removeEventListener("wheel", h);
  }, [setView]);
  const z = view.w / 1000;
  const sz = Math.sqrt(z);
  const ordered = sel === null ? edges : edges.filter((e: Ed) => e.s !== sel && e.t !== sel).concat(edges.filter((e: Ed) => e.s === sel || e.t === sel));
  const shownSorted = shown.slice().sort((a: number, b: number) => radius(NODES[a], by) - radius(NODES[b], by));
  const labels = sel !== null ? [sel].concat(Array.from(nbrs).filter((i: number) => shown.indexOf(i) >= 0).slice(0, 60)) : shownSorted.slice(-30);
  return (
    <svg ref={ref} viewBox={`${view.x} ${view.y} ${view.w} ${view.h}`} width="100%" style={{ display: "block", border: `1px solid ${theme.border.default}`, borderRadius: 12, background: theme.bg.base, cursor: "grab", userSelect: "none" }}
      onPointerDown={(e: PointerEvent<SVGSVGElement>) => { drag.current = { x: e.clientX, y: e.clientY, vx: view.x, vy: view.y, moved: false }; }}
      onPointerMove={(e: PointerEvent<SVGSVGElement>) => {
        const d = drag.current;
        if (!d || !ref.current) return;
        const dx = e.clientX - d.x;
        const dy = e.clientY - d.y;
        if (Math.abs(dx) + Math.abs(dy) > 4) d.moved = true;
        if (!d.moved) return;
        const s = view.w / ref.current.getBoundingClientRect().width;
        setView({ x: d.vx - dx * s, y: d.vy - dy * s, w: view.w, h: view.h });
      }}
      onPointerUp={() => { moved.current = drag.current ? drag.current.moved : false; drag.current = null; }}
      onPointerLeave={() => { drag.current = null; }}>
      <rect x={-2000} y={-2000} width={5000} height={5000} fill="transparent" onClick={() => { if (!moved.current) onSelect(null); }} />
      {ordered.map((e: Ed, j: number) => {
        const a = NODES[e.s];
        const b = NODES[e.t];
        const hi = sel !== null && (e.s === sel || e.t === sel);
        const money = TY[e.ty][2] === "$";
        const w = money ? 0.4 + 1.6 * Math.max(0, (Math.log10(Math.max(1, e.v)) - 2) / 6) : TFAM[e.ty] === 8 ? 1.4 : 0.8;
        return <line key={j} x1={a.x} y1={a.y} x2={b.x} y2={b.y} stroke={fcol(TFAM[e.ty])} strokeOpacity={sel === null ? 0.35 : hi ? 0.9 : 0.04} strokeWidth={w * (hi ? 1.6 : 1)} strokeDasharray={e.c === 2 ? "2 3" : e.c === 1 ? "6 3" : undefined} vectorEffect="non-scaling-stroke" />;
      })}
      {shownSorted.map((i: number) => {
        const n = NODES[i];
        const r = radius(n, by) * sz;
        const fade = sel !== null && i !== sel && !nbrs.has(i);
        const common = { fill: ncol(n), fillOpacity: fade ? 0.15 : 0.92, stroke: i === sel ? theme.text.primary : theme.bg.base, strokeWidth: i === sel ? 2 : 0.6, vectorEffect: "non-scaling-stroke" as const, style: { cursor: "pointer" }, onClick: () => { if (!moved.current) onSelect(i); } };
        let shape: ReactNode;
        if (n.k === "L") shape = <circle cx={n.x} cy={n.y} r={r} {...common} />;
        else if (n.k === "M") shape = <rect x={n.x - r * 0.9} y={n.y - r * 0.9} width={r * 1.8} height={r * 1.8} rx={r * 0.2} {...common} />;
        else if (n.k === "K") shape = <polygon points={`${n.x},${n.y - r * 1.2} ${n.x + r * 1.1},${n.y + r * 0.8} ${n.x - r * 1.1},${n.y + r * 0.8}`} {...common} />;
        else shape = <polygon points={`${n.x},${n.y - r * 1.2} ${n.x + r * 1.2},${n.y} ${n.x},${n.y + r * 1.2} ${n.x - r * 1.2},${n.y}`} {...common} />;
        return <g key={i}>{shape}<title>{`${n.name} (${KIND[n.k]})`}</title></g>;
      })}
      {labels.map((i: number) => {
        const n = NODES[i];
        const r = radius(n, by) * sz;
        return <text key={`t${i}`} x={n.x + r + 2 * z} y={n.y + 3 * z} fontSize={10 * z} fill={theme.text.primary} stroke={theme.bg.base} strokeWidth={3 * z} paintOrder="stroke" style={{ pointerEvents: "none", fontFamily: theme.font.family }}>{n.name}</text>;
      })}
    </svg>
  );
}

function props(n: Nd): { label: string; value: ReactNode }[] {
  const P = (label: string, value: string) => ({ label, value });
  const hm = (h: number, m: number) => `${h} high, ${m} medium`;
  if (n.k === "L") return [P("Firm or employer", n.sub), P("Party lean", LEAN[n.p]), P("DC influence score", `${n.sc.toFixed(1)} (rank ${mv(n, 0)})`), P("Direct + PAC money score", `${(mv(n, 1) / 10).toFixed(1)} (rank ${mv(n, 2).toLocaleString("en-US")} of 21,408)`), P("Direct-only money score", (mv(n, 3) / 10).toFixed(1)),
    P("LD-2 attributed $ 2023–26", usd(mv(n, 5) * 1000)), P("Clients, bills, agencies lobbied", `${mv(n, 6)} clients, ${mv(n, 7)} bills, ${mv(n, 8)} agencies`), P("Scored $ to members", `${usd(mv(n, 9) * 100)} to ${mv(n, 10)} members`), P("$ to PACs and committees", usd(mv(n, 11) * 100)), P("Indirect via PACs and JFCs", usd(mv(n, 12) * 100)),
    P("Former staff of current members", hm(mv(n, 13), mv(n, 14))), P("Former member of Congress", mv(n, 15) === 2 ? "Yes (high)" : mv(n, 15) === 1 ? "Yes (medium)" : "No"), P("Super PAC giving", `${usd(mv(n, 16) * 100)} high or medium, ${usd(mv(n, 25) * 100)} low`), P("FARA agent registrations", hm(mv(n, 17), mv(n, 18))),
    P("OIRA meetings", `${mv(n, 19)} high, ${mv(n, 20)} low`), P("WH visitor name matches (low)", String(mv(n, 21))), P("Hearing testimony", `${mv(n, 22)} high, ${mv(n, 23)} low`), P("990 officer or board roles", String(mv(n, 24))), P("X weighted degree", String(mv(n, 4) / 4))];
  if (n.k === "M") return [P("Seat", n.sub), P("Party", LEAN[n.p]), P("Exposure score", `${n.sc.toFixed(1)} (rank ${mv(n, 20)} of 539)`), P("Lobbyist $ incl. indirect", `${usd(memLob(n))} (rank ${mv(n, 0)}): direct ${usd(mv(n, 1) * 100)}, PACs ${usd(mv(n, 2) * 100)}, JFCs ${usd(mv(n, 3) * 100)}`), P("Lobbyists giving", String(mv(n, 4))),
    P("Independent expenditures", `${usd(mv(n, 5) * 1000)} supporting, ${usd(mv(n, 6) * 1000)} opposing`), P("Ex-staffers now lobbying", hm(mv(n, 7), mv(n, 8))), P("Clients lobbying their sponsored bills", mv(n, 9).toLocaleString("en-US")), P("FARA registrants contacting", hm(mv(n, 10), mv(n, 11))), P("FARA-reported contributions", usd(mv(n, 12) * 100)),
    P("Sponsored trips", String(mv(n, 13))), P("Lobbying companies traded or held", `${mv(n, 14)} companies, ${mv(n, 15)} transactions`), P("Committees, caucuses, CODEL partners", `${mv(n, 16)}, ${mv(n, 17)}, ${mv(n, 18)}`), P("X ties", String(mv(n, 19)))];
  if (n.k === "K") return [P("Client score", `${n.sc.toFixed(1)} (rank ${mv(n, 0)})`), P("LD-2 spend 2023–26", usd(mv(n, 1) * 1000)), P("Bills lobbied", String(mv(n, 2))), P("Members sponsoring lobbied bills", String(mv(n, 3))), P("Super PAC giving", usd(mv(n, 4) * 1000)), P("OIRA meetings", String(mv(n, 5))),
    P("Witness appearances", String(mv(n, 6))), P("Sponsored trips", String(mv(n, 7))), P("Members trading / holding", `${mv(n, 8)} / ${mv(n, 9)}`), P("Regulations.gov dockets (comments)", `${mv(n, 10)} (${mv(n, 11)})`), P("Agencies lobbied", String(mv(n, 12)))];
  if (n.k === "S") return [P("Type", n.sub), P("Lean", LEAN[n.p]), P("IE spending", usd(mv(n, 0) * 1000)), P("Received from drawn lobbyists, clients and nonprofits", usd(mv(n, 1) * 100))];
  if (n.k === "C") return [P("Committee type", n.sub), P("Lean", LEAN[n.p]), P("$ from universe lobbyists", usd(mv(n, 0) * 100)), P("Lobbyists giving", String(mv(n, 1)))];
  if (n.k === "F") return [P("Country", n.sub), P("Government principal", mv(n, 1) ? "Yes" : "No"), P("Current members in contact reports", String(mv(n, 0)))];
  if (n.k === "W") return [P("Bill", n.sub), P("Sponsor party", LEAN[n.p]), P("Clients lobbying it", String(mv(n, 0))), P("Became law", mv(n, 1) ? "Yes" : "No")];
  const lab: Record<string, string> = { N: "Flow total ($K)", R: "Members mentioned", A: "LD-2 + OIRA reports", H: "Committee seats", U: "Members", B: "Bundled ($K)" };
  if (n.k === "N" && n.sub === "Travel sponsor") return [P("Type", "Travel sponsor (trip counts are on its edges)")];
  return [P("Type", n.sub || KIND[n.k]), P(lab[n.k] || "Score", mv(n, 0).toLocaleString("en-US"))];
}

export default function App() {
  const theme = useGrokTheme();
  const dv = theme.dataviz;
  const cat = dv.categorical;
  const pcol = (p: string): string => p === "R" ? dv.negative : p === "D" ? cat[0] : p === "I" ? cat[2 % cat.length] : p === "M" ? cat[1 % cat.length] : dv.other;
  const KC: Record<string, number> = { K: 3, N: 5, F: 4, R: 4, A: 6, H: 7, W: 1, U: 2, B: 1 };
  const ncol = (n: Nd): string => "LMSC".indexOf(n.k) >= 0 ? pcol(n.p) : cat[KC[n.k] % cat.length];
  const FC = [1, 3, 2, 4, 5, 6, 7, 8, -1];
  const fcol = (f: number): string => FC[f] < 0 ? theme.text.secondary : cat[FC[f] % cat.length];
  const [famOn, setFamOn] = useState<boolean[]>(FAM.map(() => true));
  const [tyOn, setTyOn] = useState<boolean[]>(TY.map(() => true));
  const [detail, setDetail] = useState<boolean>(false);
  const [conf, setConf] = useState<string>("0");
  const [minUsd, setMinUsd] = useState<string>("0");
  const [minScore, setMinScore] = useState<string>("0");
  const [mParty, setMParty] = useState<string>("all");
  const [lean, setLean] = useState<string>("all");
  const [by, setBy] = useState<string>("dc");
  const [sel, setSel] = useState<number | null>(null);
  const [q, setQ] = useState<string>("");
  const [view, setView] = useState<View>(FULL);
  const [lSort, setLSort] = useState<string>("dc");
  const [lAll, setLAll] = useState<boolean>(false);
  const [mSort, setMSort] = useState<string>("exp");
  const [mAll, setMAll] = useState<boolean>(false);
  const [kAll, setKAll] = useState<boolean>(false);

  const cl = Number(conf);
  const minU = Number(minUsd) || 0;
  const minS = Number(minScore) || 0;
  const nodeOk = (n: Nd): boolean => n.k === "L" ? (lean === "all" || n.p === lean) && n.sc >= minS : n.k === "M" ? mParty === "all" || n.p === mParty : true;
  const visEdges = EDGES.filter((e: Ed) => famOn[TFAM[e.ty]] && tyOn[e.ty] && e.c <= cl && (TY[e.ty][2] !== "$" || e.v >= minU) && nodeOk(NODES[e.s]) && nodeOk(NODES[e.t]));
  const shownSet = new Set<number>();
  visEdges.forEach((e: Ed) => { shownSet.add(e.s); shownSet.add(e.t); });
  if (sel !== null && NODES[sel].d) shownSet.add(sel);
  const shown = Array.from(shownSet);
  const tyCount = TY.map((_t: string[], j: number) => visEdges.filter((e: Ed) => e.ty === j).length);
  const famCount = FAM.map((_f: string, j: number) => visEdges.filter((e: Ed) => TFAM[e.ty] === j).length);
  const nbrs = new Set<number>();
  const ties: Ed[] = [];
  if (sel !== null) EDGES.forEach((e: Ed) => { if (e.s === sel || e.t === sel) { ties.push(e); nbrs.add(e.s === sel ? e.t : e.s); } });
  const focus = (i: number) => {
    const n = NODES[i];
    setSel(i);
    if (n.d) setView({ x: n.x - 300, y: n.y - 210, w: 600, h: 420 });
    if (typeof document !== "undefined") { const el = document.getElementById("map"); if (el) el.scrollIntoView({ behavior: "smooth", block: "start" }); }
  };
  const nameCell = (n: Nd): ReactNode => <span style={{ cursor: "pointer", textDecoration: "underline", textDecorationColor: theme.border.strong, textUnderlineOffset: 3 }} onClick={() => focus(n.i)}>{n.name}</span>;
  const zoomBy = (k: number) => { const w = Math.min(1400, Math.max(60, view.w * k)); setView({ x: view.x + (view.w - w) / 2, y: view.y + (view.h - w * 0.7) / 2, w, h: w * 0.7 }); };
  const qq = q.trim().toLowerCase();
  const matches = qq.length >= 2 ? NODES.filter((n: Nd) => n.name.toLowerCase().includes(qq)).slice(0, 10) : [];
  const preset = (f: number[] | null) => setFamOn(FAM.map((_f: string, j: number) => f === null || f.indexOf(j) >= 0));
  const selN = sel !== null ? NODES[sel] : null;

  const lKey = (n: Nd): number => lSort === "money" ? mv(n, 1) : lSort === "d" ? mv(n, 3) : lSort === "ld2" ? mv(n, 5) : lSort === "usd" ? mv(n, 9) : lSort === "rev" ? mv(n, 13) * 2 + mv(n, 14) : lSort === "x" ? mv(n, 4) : n.sc;
  const lRows = LOBS.slice().sort((a: Nd, b: Nd) => lKey(b) - lKey(a)).slice(0, lAll ? 999 : 50).map((n: Nd, i: number) => [String(i + 1), nameCell(n), n.sub, n.p, `${n.sc.toFixed(1)} (#${mv(n, 0)})`, `${(mv(n, 1) / 10).toFixed(1)} (#${mv(n, 2)})`, (mv(n, 3) / 10).toFixed(1), usd(mv(n, 5) * 1000), usd(mv(n, 9) * 100), String(mv(n, 6)), String(mv(n, 7)), `${mv(n, 13)}/${mv(n, 14)}`, `${mv(n, 17)}/${mv(n, 18)}`, String(mv(n, 19)), String(mv(n, 4) / 4), n.d ? "Drawn" : "Indexed"]);
  const mKey = (n: Nd): number => mSort === "lob" ? memLob(n) : mSort === "ie" ? mv(n, 5) + mv(n, 6) : mSort === "staff" ? mv(n, 7) * 2 + mv(n, 8) : mSort === "fara" ? mv(n, 10) * 2 + mv(n, 11) : mSort === "trade" ? mv(n, 15) : mSort === "trips" ? mv(n, 13) : n.sc;
  const mRows = MEMS.slice().sort((a: Nd, b: Nd) => mKey(b) - mKey(a)).slice(0, mAll ? 999 : 50).map((n: Nd) => [String(mv(n, 20)), nameCell(n), n.p, n.sub, n.sc.toFixed(1), usd(memLob(n)), usd(mv(n, 5) * 1000), usd(mv(n, 6) * 1000), `${mv(n, 7)}/${mv(n, 8)}`, mv(n, 9).toLocaleString("en-US"), `${mv(n, 10)}/${mv(n, 11)}`, String(mv(n, 13)), String(mv(n, 15)), String(mv(n, 19)), n.d ? "Drawn" : "Indexed"]);
  const kRows = CLIS.slice().sort((a: Nd, b: Nd) => b.sc - a.sc).slice(0, kAll ? 999 : 40).map((n: Nd) => [String(mv(n, 0)), nameCell(n), n.sc.toFixed(1), usd(mv(n, 1) * 1000), String(mv(n, 2)), String(mv(n, 3)), usd(mv(n, 4) * 1000), String(mv(n, 5)), String(mv(n, 6)), String(mv(n, 7)), `${mv(n, 8)}/${mv(n, 9)}`, n.d ? "Drawn" : "Indexed"]);
  const top = (k: string, f: (n: Nd) => number, c: number): Nd[] => NODES.filter((n: Nd) => n.k === k).sort((a: Nd, b: Nd) => f(b) - f(a)).slice(0, c);
  const kindRows = KORD.split("").map((k: string) => { const all = NODES.filter((n: Nd) => n.k === k); const dr = all.filter((n: Nd) => n.d).length; return [KIND[k], String(dr), String(all.length - dr), String(all.length)]; });
  const famRows = FAM.map((f: string, j: number) => [f, TY.map((t: string[], k: number) => (TFAM[k] === j ? `${t[0]} ${EDGES.filter((e: Ed) => e.ty === k).length}` : "")).filter((s: string) => s).join(" · "), String(EDGES.filter((e: Ed) => TFAM[e.ty] === j).length)]);
  const nDrawn = NODES.filter((n: Nd) => n.d).length;
  const swatch = (c: string, label: string, shape: string) => (
    <span key={label + shape} style={{ display: "inline-flex", alignItems: "center", gap: 6, color: theme.text.secondary, fontSize: 13 }}>
      <svg width="12" height="12" viewBox="0 0 12 12">{shape === "c" ? <circle cx="6" cy="6" r="5" fill={c} /> : shape === "s" ? <rect x="1" y="1" width="10" height="10" rx="2" fill={c} /> : shape === "t" ? <polygon points="6,0 12,11 0,11" fill={c} /> : shape === "l" ? <line x1="0" y1="6" x2="12" y2="6" stroke={c} strokeWidth="2.5" /> : <polygon points="6,0 12,6 6,12 0,6" fill={c} />}</svg>{label}
    </span>
  );

  return (
    <Page title="DC influence map: lobbyists, money and Congress" summary="One map of every public layer collected so far: lobbying, money, the revolving door, foreign agents, outside and dark money, legislative, executive, ethics and travel, and social ties, for 21,408 lobbyists and 539 members of Congress." width="full" sources={["https://github.com/413x45h4w/gop-lobby-graph", "https://lda.gov (LD-2 and LD-203, 2023Q1–2026Q3)", "https://www.fec.gov/data/browse-data/?tab=bulk-data and OpenFEC (contributions, IEs, committees)", "https://efile.fara.gov (FARA registrations and supplemental statements)", "IRS Form 990 e-file and Form 8872 (527s); SEC proxy filings (boards)", "https://api.congress.gov and House and Senate committee hearing records", "https://www.reginfo.gov (OIRA EO 12866 meetings), https://www.regulations.gov (sampled), Biden-era WH visitor logs", "House and Senate financial disclosures, travel and CODEL reports", "X posts through the 2026-11-22 run; Instagram batches through 2026-11-22"]}>
      <TableOfContents items={[{ label: "Summary", id: "summary" }, { label: "Influence map", id: "map" }, { label: "Drawn vs indexed", id: "drawn" }, { label: "Headline findings by layer", id: "find" }, { label: "Cross-layer scores", id: "scores" }, { label: "Top entities", id: "top" }, { label: "Lobbyist rankings", id: "lrank" }, { label: "Member rankings", id: "mrank" }, { label: "Client rankings", id: "krank" }, { label: "Money by party", id: "party" }, { label: "Sources, gaps and caveats", id: "caveats" }]} />
      <Section heading="Summary" id="summary">
        <Metrics metrics={[
          { value: "21,408", label: "Lobbyists", detail: "LD-2 2023Q1–2026Q3 plus LD-203-only filers" },
          { value: "539", label: "Members of Congress", detail: "Current, incl. delegates" },
          { value: "297,355", label: "LD-2 reports", detail: "24,204 clients; 82,676 name bills" },
          { value: "$139.34M", label: "Scored direct lobbyist money", detail: "Plus $88.74M to committees, $25.20M indirect" },
          { value: "$1.99B", label: "IEs targeting current members", detail: "Of $7.70B non-excluded IE spending" },
          { value: "8,858", label: "Ex-staffer lobbying pairs", detail: "2,445 confirmed by two sources" },
          { value: "17,641", label: "FARA contact or mention rows", detail: "From 3,062 supplemental statements" },
          { value: `${nDrawn} / ${NODES.length}`, label: "Entities drawn / indexed", detail: `${EDGES.length.toLocaleString("en-US")} edges drawn in 46 types` },
        ]} />
        <Callout lead="Takeaway">Adding the new layers reshuffles the top. On the cross-layer DC score, former senator John Breaux (Crossroads Strategies) ranks first although he is #761 on money alone, because of $4.17M in attributed LD-2 lobbying, 51 clients, 136 bills and his former-member status. Sen. John Cornyn and Rep. French Hill have the most exposure across layers, and trade associations (API, NAR, the American Chemistry Council) top the client ranking. Foreign outreach is broad but shallow: the Korean and Kazakh embassies' FARA reports mention more than 490 members each.</Callout>
      </Section>
      <Section heading="Influence map" id="map">
        <div style={{ display: "flex", flexWrap: "wrap", gap: 12, alignItems: "flex-end" }}>
          <div style={{ minWidth: 200, flex: "1 1 200px" }}><Input label="Search any entity (drawn or indexed)" value={q} onChange={(v: string) => setQ(v)} placeholder="e.g. Breaux, Cornyn, Fairshake, Qatar" /></div>
          <div style={{ minWidth: 130 }}><Select label="Member party" value={mParty} onChange={(v: string) => setMParty(v)} options={[{ value: "all", label: "All" }, { value: "R", label: "Republican" }, { value: "D", label: "Democrat" }, { value: "I", label: "Independent" }]} /></div>
          <div style={{ minWidth: 130 }}><Select label="Lobbyist lean" value={lean} onChange={(v: string) => setLean(v)} options={[{ value: "all", label: "All" }, { value: "R", label: "Republican" }, { value: "D", label: "Democrat" }, { value: "M", label: "Mixed" }, { value: "U", label: "Unknown" }]} /></div>
          <div style={{ width: 140 }}><Input label="Min $ per money edge" type="number" value={minUsd} onChange={(v: string) => setMinUsd(v)} /></div>
          <div style={{ width: 140 }}><Input label="Min lobbyist DC score" type="number" value={minScore} onChange={(v: string) => setMinScore(v)} /></div>
          <div style={{ minWidth: 150 }}><Select label="Size L, M, K by" value={by} onChange={(v: string) => setBy(v)} options={[{ value: "dc", label: "Cross-layer score" }, { value: "money", label: "Money score (lobbyists)" }]} /></div>
        </div>
        <div style={{ display: "flex", flexWrap: "wrap", gap: 12, alignItems: "center" }}>
          <Segmented value={conf} onChange={(v: string) => setConf(v)} options={[{ value: "0", label: "High confidence" }, { value: "1", label: "+ Medium" }, { value: "2", label: "+ Low" }]} />
          <Button label="All families" onClick={() => preset(null)} />
          <Button label="Money" onClick={() => preset([0])} />
          <Button label="Lobbying + revolving" onClick={() => preset([1, 2])} />
          <Button label="Foreign" onClick={() => preset([3])} />
          <Button label="Outside money" onClick={() => preset([4])} />
          <Button label="Zoom in" onClick={() => zoomBy(0.7)} />
          <Button label="Zoom out" onClick={() => zoomBy(1 / 0.7)} />
          <Button label="Reset view" onClick={() => { setView(FULL); setSel(null); }} />
        </div>
        {matches.length > 0 ? <div style={{ display: "flex", flexWrap: "wrap", gap: 8 }}>{matches.map((n: Nd) => <Button key={n.i} label={`${n.name} · ${KIND[n.k]}${n.d ? "" : " · indexed"}`} onClick={() => { focus(n.i); setQ(""); }} />)}</div> : null}
        <div style={{ display: "flex", flexWrap: "wrap", gap: "6px 18px" }}>
          {FAM.map((f: string, j: number) => <div key={f} style={{ display: "inline-flex", alignItems: "center", gap: 6 }}>{swatch(fcol(j), "", "l")}<Toggle label={`${f} (${famCount[j]})`} value={famOn[j]} onChange={(v: boolean) => setFamOn(famOn.map((x: boolean, k: number) => (k === j ? v : x)))} /></div>)}
          <Toggle label="Edit single layers" value={detail} onChange={(v: boolean) => setDetail(v)} />
        </div>
        {detail ? <div style={{ display: "flex", flexWrap: "wrap", gap: "4px 16px" }}>{TY.map((t: string[], j: number) => <Toggle key={t[0]} label={`${FAM[TFAM[j]]}: ${t[0]} (${tyCount[j]})`} value={tyOn[j]} onChange={(v: boolean) => setTyOn(tyOn.map((x: boolean, k: number) => (k === j ? v : x)))} />)}</div> : null}
        <div style={{ display: "flex", flexWrap: "wrap", gap: "6px 16px" }}>
          {swatch(pcol("R"), "Republican", "c")}{swatch(pcol("D"), "Democrat", "c")}{swatch(pcol("I"), "Independent", "c")}{swatch(pcol("M"), "Mixed lean", "c")}{swatch(pcol("U"), "Unknown lean", "c")}
          {swatch(theme.text.tertiary, "Lobbyist", "c")}{swatch(theme.text.tertiary, "Member", "s")}{swatch(cat[3 % cat.length], "Client or company", "t")}
          {["N", "F", "A", "H", "W", "U"].map((k: string) => swatch(cat[KC[k] % cat.length], KIND[k], "d"))}
          {swatch(theme.text.tertiary, "Super PAC, PAC (party colour)", "d")}
        </div>
        <NetworkSvg view={view} setView={setView} edges={visEdges} shown={shown} sel={sel} nbrs={nbrs} onSelect={(i: number | null) => setSel(i)} ncol={ncol} fcol={fcol} by={by} theme={theme} />
        <Text>{`Showing ${shown.length} nodes and ${visEdges.length} of ${EDGES.length} edges. Edge colour is the layer family; solid lines are high confidence, long dashes medium, short dashes low. Click a node for its sphere, drag to pan, and pinch or Ctrl/⌘ + scroll to zoom. The default shows high-confidence ties only, so medium-only layers (caucuses, foreign principal → registrant, org testimony) appear when you choose + Medium, and White House visitor matches only at + Low.`}</Text>
        {selN ? (
          <Section heading={`Sphere: ${selN.name} (${KIND[selN.k]})`}>
            {selN.d ? null : <Callout lead="Indexed only">This entity is not drawn on the map. The totals below come from the full dataset.</Callout>}
            <Properties items={props(selN)} />
            {FAM.map((f: string, j: number) => {
              const fe = ties.filter((e: Ed) => TFAM[e.ty] === j).sort((a: Ed, b: Ed) => a.c - b.c || b.v - a.v);
              if (fe.length === 0) return null;
              return (
                <Section key={f} heading={`${f}: ${fe.length} drawn ties`}>
                  <Table columns={["Connected to", "Kind", "Party or lean", "Tie", "Value", "Confidence"]} align={["start", "start", "start", "start", "end", "start"]}
                    rows={fe.slice(0, 40).map((e: Ed) => { const o = NODES[e.s === sel ? e.t : e.s]; return [nameCell(o), KIND[o.k], LEAN[o.p] || "", (e.s === sel ? "" : "← ") + TY[e.ty][0], fmtV(e), CONF[e.c]]; })} />
                </Section>
              );
            })}
            <Text>Drawn ties are capped per entity (see Drawn vs indexed); the property totals above are complete.</Text>
          </Section>
        ) : null}
      </Section>
      <Section heading="Drawn vs indexed" id="drawn" caption="Indexed entities can be searched and opened in the sphere panel, with full totals, but are not drawn.">
        <Grid columns={2}>
          <Table columns={["Kind", "Drawn", "Indexed only", "Total"]} align={["start", "end", "end", "end"]} rows={kindRows} />
          <Table columns={["Family", "Edges drawn by type", "Total"]} align={["start", "start", "end"]} rows={famRows} />
        </Grid>
        <Text>Drawn core: 257 lobbyists (top 150 by DC score, top 20 by money score, Jeffrey Miller, and every lobbyist with an accepted X tie), 308 members (top 280 by exposure plus every member with an X tie), the top 90 clients by client score, and the PACs, super PACs, nonprofits, foreign principals, registrants, agencies, committees, top 30 bills and top 8 caucuses those ties reach. Indexed only: the other 231 members, lobbyists ranked up to 220 on DC score and clients up to rank 130.</Text>
        <Text>Weak edges are trimmed. Per lobbyist: top 3 direct gifts of $2,000 or more, top 2 PAC-indirect ($250+), top JFC ($1,000+) and top committee ($500+), top 2 clients, top 3 ex-staff ties. Per client: top member whose bills it lobbied, top agency, top OIRA agency, top docket, top committee testified to. Per IE spender, the 5 biggest targets; per registrant, 6 members contacted and 4 contributions; per travel sponsor, 5 members; per member, top 2 traded and top held lobbying companies. Cosponsorship shows the 50 strongest cross-party and 50 same-party pairs, CODELs the top 50 pairs.</Text>
      </Section>
      <Section heading="Headline findings by layer" id="find">
        <Rows rows={[
          { lead: "Lobbying", title: "297,355 LD-2 reports from 24,204 clients; 82,676 (28%) name bills", detail: "The U.S. Chamber of Commerce reports the most in-house spend ($265.65M). Rep. Jodey Arrington's sponsored bills were lobbied by 2,773 clients, then Reps. Tom Cole (1,623) and Mike Rogers (1,541)." },
          { lead: "Revolving door", title: "8,858 lobbyist–member former-staff pairs (5,140 lobbyists, 476 current members)", detail: "2,445 pairs are confirmed by two sources. Most ex-staff lobbying (high + medium): Schumer 33 + 23, McConnell 31 + 19, Collins 25 + 20, Cornyn 25 + 18. 263 former members lobby, 97 at high confidence." },
          { lead: "Foreign", title: "3,062 FARA statements, 17,641 contact or mention rows", detail: "The Embassy of the Republic of Korea's filings mention 515 current members and Kazakhstan's 493, mostly through Brownstein Hyatt (516 members). FARA-reported contributions: 11,147 totalling $13.5M linked to 675 members. Most-mentioned members: Cruz (48 high), Joe Wilson (46), Meeks (45)." },
          { lead: "Outside money", title: "$7.70B of IEs; $1.99B targeted current members ($0.90B 2024, $1.09B 2026)", detail: "Sen. Jon Husted drew the most: $129.7M opposing, $67.8M supporting; then Bernie Moreno ($85.5M opposing, $58.8M supporting). Biggest spenders: WinSenate $294M, HMP (House Majority PAC) $227M, Defend American Jobs $121M, AFP Action $82M." },
          { lead: "Super PACs", title: "1,282 lobbyists gave $4.69M to super PACs ($3.53M high confidence)", detail: "Organisations that hire lobbyists gave $1.20B, led by Coinbase to Fairshake ($68.5M in 2024)." },
          { lead: "Dark money", title: "1,463 Form 990s parsed; $34.2B in unflagged grants", detail: "Future Forward USA Action passed $266M to Future Forward PAC and Stand Together Chamber $121M to AFP. Largest 527s: DGA $389M, RGA $315M. Donor names on 990s are redacted." },
          { lead: "Boards", title: "198 public companies, 2,212 board seats, 216 interlocking directors", detail: "6 former members sit on boards; no current lobbyists matched." },
          { lead: "Legislative", title: "7,217 hearings with 22,423 witness rows, 1,153 of them lobbyists", detail: "3,895 committee roster edges and 115,313 member cosponsorship pairs." },
          { lead: "Executive", title: "3,277 OIRA meetings; 56,396 sampled regulations.gov comments on 83 dockets", detail: "6,856 White House visitor-log name matches are kept at low confidence only." },
          { lead: "Ethics", title: "20,151 stock transactions and 1,941 holding edges to lobbying companies", detail: "Rep. Josh Gottheimer made 796 transactions in companies that lobby, Sen. Tommy Tuberville 483. 4,427 sponsored-travel edges: Congressional Institute paid for 1,181 trips; 6,105 of 7,193 trips were by staff. Speaker Mike Johnson took the most member trips (134)." },
          { lead: "Caucus and CODEL", title: "1,402 caucus memberships; 2,952 House and 149 Senate CODEL pairs", detail: "Caucus data is medium confidence." },
          { lead: "Social", title: "X through the Nov 22 run: 147 rows, 134 weighted, 114 pairs", detail: "97 lobbyists and 78 members; coverage 4,135 of 20,225 queued lobbyists (20.4%). Instagram: 13 member tags from @miller_strategies." },
        ]} />
      </Section>
      <Section heading="Cross-layer scores" id="scores" caption="Each part is the percentile among entities with a positive value (ties averaged, zero scores 0). Score = 100 × Σ weight × percentile. Money scores are kept and shown beside it.">
        <Grid columns={3}>
          <Table columns={["Lobbyist DC score", "Weight"]} align={["start", "end"]} rows={[["Money (direct + PAC score)", ".35"], ["LD-2 attributed $", ".15"], ["Bills lobbied", ".10"], ["Revolving door (ex-staff high + ½ medium, +3 if former member)", ".10"], ["Clients", ".05"], ["OIRA meetings (high)", ".05"], ["Super PAC $ (high + medium)", ".05"], ["FARA agent registrations", ".05"], ["X weight", ".05"], ["Testimony (high)", ".025"], ["990 officer or board", ".025"]]} />
          <Table columns={["Member exposure", "Weight"]} align={["start", "end"]} rows={[["Lobbyist $ incl. indirect", ".30"], ["IEs supporting + opposing", ".15"], ["Ex-staff lobbying (high + ½ medium)", ".15"], ["Clients lobbying their sponsored bills", ".15"], ["FARA registrants (high + ½ medium)", ".10"], ["Sponsored trips", ".05"], ["Lobbying companies traded or held", ".05"], ["X ties", ".05"]]} />
          <Table columns={["Client score", "Weight"]} align={["start", "end"]} rows={[["LD-2 spend", ".40"], ["Members sponsoring lobbied bills", ".15"], ["Super PAC $", ".15"], ["OIRA meetings", ".10"], ["Witness appearances", ".05"], ["Sponsored travel", ".05"], ["Members trading or holding", ".05"], ["Bills lobbied", ".05"]]} />
        </Grid>
      </Section>
      <Section heading="Top entities" id="top">
        <Grid columns={2}>
          <Section heading="Lobbyists by DC score"><Table columns={["Lobbyist", "Firm", "DC", "Money (rank)"]} align={["start", "start", "end", "end"]} rows={top("L", (n: Nd) => n.sc, 10).map((n: Nd) => [nameCell(n), n.sub, n.sc.toFixed(1), `${(mv(n, 1) / 10).toFixed(1)} (#${mv(n, 2)})`])} /></Section>
          <Section heading="Members by exposure"><Table columns={["Member", "Seat", "Exposure", "Lobbyist $"]} align={["start", "start", "end", "end"]} rows={top("M", (n: Nd) => n.sc, 10).map((n: Nd) => [nameCell(n), `${n.p} · ${n.sub}`, n.sc.toFixed(1), usdM(memLob(n))])} /></Section>
          <Section heading="Clients by client score"><Table columns={["Client", "Score", "LD-2 $"]} align={["start", "end", "end"]} rows={top("K", (n: Nd) => n.sc, 10).map((n: Nd) => [nameCell(n), n.sc.toFixed(1), usdM(mv(n, 1) * 1000)])} /></Section>
          <Section heading="IE spenders on the map"><Bars bars={top("S", (n: Nd) => mv(n, 0), 10).map((n: Nd) => ({ label: n.name, value: mv(n, 0), display: usdM(mv(n, 0) * 1000), meta: LEAN[n.p] }))} /></Section>
          <Section heading="Foreign principals by members in contact reports"><Bars bars={top("F", (n: Nd) => mv(n, 0), 10).map((n: Nd) => ({ label: n.name, value: mv(n, 0), display: String(mv(n, 0)), meta: n.sub }))} /></Section>
          <Section heading="Members by lobbyist $ incl. indirect"><Bars bars={top("M", memLob, 10).map((n: Nd) => ({ label: n.name, value: memLob(n), display: usdM(memLob(n)), meta: `${n.p} · ${n.sub}` }))} /></Section>
        </Grid>
      </Section>
      <Section heading="Lobbyist rankings" id="lrank" caption="All drawn and indexed lobbyists. Ex-staff and FARA columns are high/medium.">
        <div style={{ display: "flex", flexWrap: "wrap", gap: 12, alignItems: "center" }}>
          <Segmented value={lSort} onChange={(v: string) => setLSort(v)} options={[{ value: "dc", label: "DC score" }, { value: "money", label: "Direct + PAC" }, { value: "d", label: "Direct only" }, { value: "ld2", label: "LD-2 $" }, { value: "usd", label: "$ to members" }, { value: "rev", label: "Ex-staff" }, { value: "x", label: "X" }]} />
          <Toggle label={`Show all ${LOBS.length}`} value={lAll} onChange={(v: boolean) => setLAll(v)} />
        </div>
        <Table columns={["#", "Lobbyist", "Firm", "Lean", "DC (rank)", "D+PAC (rank)", "Direct", "LD-2 $", "$ to members", "Clients", "Bills", "Ex-staff", "FARA", "OIRA", "X", "Map"]} align={["end", "start", "start", "start", "end", "end", "end", "end", "end", "end", "end", "end", "end", "end", "end", "start"]} rows={lRows} />
      </Section>
      <Section heading="Member rankings" id="mrank" caption="All 539 members; rank is by exposure score. Ex-staff and FARA columns are high/medium.">
        <div style={{ display: "flex", flexWrap: "wrap", gap: 12, alignItems: "center" }}>
          <Segmented value={mSort} onChange={(v: string) => setMSort(v)} options={[{ value: "exp", label: "Exposure" }, { value: "lob", label: "Lobbyist $" }, { value: "ie", label: "IEs" }, { value: "staff", label: "Ex-staff" }, { value: "fara", label: "FARA" }, { value: "trips", label: "Trips" }, { value: "trade", label: "Trades" }]} />
          <Toggle label="Show all 539" value={mAll} onChange={(v: boolean) => setMAll(v)} />
        </div>
        <Table columns={["Rank", "Member", "Party", "Seat", "Exposure", "Lobbyist $", "IE for", "IE against", "Ex-staff", "Clients on bills", "FARA", "Trips", "Trades", "X", "Map"]} align={["end", "start", "start", "start", "end", "end", "end", "end", "end", "end", "end", "end", "end", "end", "start"]} rows={mRows} />
      </Section>
      <Section heading="Client rankings" id="krank" caption="Clients and companies that hire lobbyists. Trade/hold counts members.">
        <Toggle label={`Show all ${CLIS.length}`} value={kAll} onChange={(v: boolean) => setKAll(v)} />
        <Table columns={["Rank", "Client", "Score", "LD-2 $", "Bills", "Sponsors", "Super PAC $", "OIRA", "Witness", "Travel", "Trade/hold", "Map"]} align={["end", "start", "end", "end", "end", "end", "end", "end", "end", "end", "end", "start"]} rows={kRows} />
      </Section>
      <Section heading="Money by party" id="party" caption="$ millions, unchanged money layers (built 2026-11-18). Committee money is grouped by committee lean.">
        <ColumnSeries labels={["Direct (scored)", "To committees", "PAC indirect", "JFC indirect", "Form 3L bundling"]} series={[{ name: "Republican", values: [84.09, 39.33, 9.84, 5.93, 0.30] }, { name: "Democrat", values: [55.00, 27.86, 6.24, 3.13, 23.03] }, { name: "Other", values: [0.25, 21.55, 0.06, 0.0, 0.0] }]} format={(v: number) => "$" + v.toFixed(2) + "M"} />
      </Section>
      <Section heading="Sources, gaps and caveats" id="caveats">
        <Rows rows={[
          { lead: "White House", title: "The current administration does not publish visitor logs", detail: "Only Biden-era logs exist; the 6,856 kept rows are name matches, low-confidence leads only, shown at + Low." },
          { lead: "Regulations.gov", title: "Comments are sampled", detail: "56,396 comments from 83 dockets, not the full record." },
          { lead: "Unavailable", title: "OpenSecrets, FollowTheMoney and Political Party Time could not be used; LegiStorm is paywalled", detail: "Fundraiser invitations and state money are not covered, and staff histories come from LD-2 covered positions and public bios." },
          { lead: "990s", title: "Donor names are redacted", detail: "Dark-money flows are traced only from grantor to grantee and Schedule C. The 87 990 officer rows that match former members (78 people, such as DeMint, Meadows and Zeldin) are about 75–80% precise and medium confidence; former members are not member nodes, so they are not drawn." },
          { lead: "FARA", title: "Counts are mentions, not meetings", detail: "A supplemental statement listing a member's office is a reported contact or outreach. Embassy outreach lists of hundreds of members are mass mailings." },
          { lead: "Holdings", title: "Sen. Jim Justice's Blackstone holding was a false match and is excluded", detail: "The asset is Blackstone Energy LLC (coal mining, Roanoke, Va.), not Blackstone Group; there was no Blackstone trade." },
          { lead: "Bills", title: "97% of LD-2 bill references use an inferred Congress", detail: "Bill edges are drawn only where the bill is found in Congress.gov bill status." },
          { lead: "Money", title: "PAC and JFC flows are pro rata estimates", detail: "Each contribution counts up to $7,000; LD-2 income is split equally among a filing's lobbyists; in-house figures are whole-organisation spend." },
          { lead: "Matching", title: "Names plus employer, registrant or caption evidence; no facial recognition", detail: "Organisations are matched by normalised name across LD-2, FEC, OIRA, 990 and disclosure files, so some related entities are merged or split." },
          { lead: "Dates", title: "Data as of November 22, 2026", detail: "LDA filings 2023Q1–2026Q3; FEC files dated 2026-11-15 to 11-18; new layers pulled 2026-11-22; X through the 2026-11-22 run; map rebuilt 2026-11-22." },
        ]} />
      </Section>
    </Page>
  );
}
