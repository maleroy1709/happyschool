from django.conf.urls import url

from . import views

urlpatterns = [
    url(r'^$', views.index, name='dossier_eleve'),
    url(r'^gen_pdf/$', views.gen_pdf, name='gen_pdf'),
    url(r'^nouveau_cas/$', views.nouveau_cas, name='nouveau_cas'),
    url(r'^nouveau_cas/(?P<cas_id>[0-9]+)$', views.nouveau_cas, name='nouveau_cas'),
    url(r'^stats/(?P<matricule>[0-9]+)$', views.get_stats, name='get_stats'),
    url(r'^get_entries/$', views.get_entries, name='get_entries'),
    url(r'^get_entries/(?P<ens>\w+)/(?P<column>\w+)/$', views.get_entries, name='get_entries'),
    url(r'^get_cas/$', views.get_cas, name='get_cas'),
    url(r'^get_pdf/(?P<all_year>[0-9]+)/(?P<matricule>[0-9]+)/(?P<infos>[0-9]+)/(?P<sanctions>[0-9]+)/',
        views.get_pdf, name='get_pdf'),
    url(r'^get_pdf/(?P<all_year>[0-9]+)/(?P<classe>\w+)/', views.get_pdf, name='get_pdf'),
    url(r'^get_pdf/', views.get_pdf, name='get_pdf'),
    url(r'^get_pdf_council/(?P<date_from>.*)/(?P<date_to>.*)/', views.get_pdf_council, name='get_pdf_council'),
    url(r'^get_pdf_council/', views.get_pdf_council, name='get_pdf_council'),
    url(r'^get_pdf_retenues/(?P<date>.*)', views.get_pdf_retenues, name='get_pdf_retenues'),
    url(r'^get_pdf_retenues/', views.get_pdf_retenues, name='get_pdf_retenues'),
    url(r'^change_sanction/(?P<cas_id>[0-9]+)/(?P<is_done>[0-9]+)$', views.change_sanction, name='change_sanction'),
    url(r'^change_sanction/', views.change_sanction, name='change_sanction'),
#    url(r'^ajouter_malade$', views.ajouter_malade, name='ajouter_malade'),
#    url(r'^encoder_sortie/(?P<passageId>[0-9]+)$', views.encoder_sortie, name='encoder_sortie'),
]