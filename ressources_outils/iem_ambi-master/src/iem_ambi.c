/* For information on usage and redistribution, and for a DISCLAIMER OF ALL
* WARRANTIES, see the file, "LICENSE.txt," in this distribution.

iem_ambi written by Thomas Musil, Copyright (c) IEM KUG Graz Austria 2000 - 2018 */

#include "m_pd.h"
#include "iemlib.h"

static t_class *iem_ambi_class;

static void *iem_ambi_new(void)
{
	t_object *x = (t_object *)pd_new(iem_ambi_class);

	return (x);
}

void ambi_encode_setup(void);
void ambi_decode_setup(void);
void ambi_decode2_setup(void);
void ambi_decode3_setup(void);
void ambi_decode_cube_setup(void);
void ambi_rot_setup(void);

void bin_ambi_calc_HRTF_setup(void);
void bin_ambi_reduced_decode_setup(void);
void bin_ambi_reduced_decode2_setup(void);
void bin_ambi_reduced_decode_fft_setup(void);
void bin_ambi_reduced_decode_fir_setup(void);
void bin_ambi_reduced_decode_fft2_setup(void);
void bin_ambi_reduced_decode_fir2_setup(void);

void matrix_mul_line_tilde_setup(void);
void matrix_mul_line8_tilde_setup(void);
void matrix_mul_stat_tilde_setup(void);
void matrix_diag_mul_line_tilde_setup(void);
void matrix_diag_mul_line8_tilde_setup(void);
void matrix_diag_mul_stat_tilde_setup(void);
void matrix_bundle_line_tilde_setup(void);
void matrix_bundle_line8_tilde_setup(void);
void matrix_bundle_stat_tilde_setup(void);

/* ------------------------ setup routine ------------------------- */

void iem_ambi_setup(void)
{
  ambi_encode_setup();
	ambi_decode_setup();
	ambi_decode2_setup();
	ambi_decode3_setup();
	ambi_decode_cube_setup();
	ambi_rot_setup();

  bin_ambi_calc_HRTF_setup();
	bin_ambi_reduced_decode_setup();
	bin_ambi_reduced_decode2_setup();
	bin_ambi_reduced_decode_fft_setup();
	bin_ambi_reduced_decode_fir_setup();
	bin_ambi_reduced_decode_fft2_setup();
	bin_ambi_reduced_decode_fir2_setup();

  matrix_mul_line_tilde_setup();
  matrix_mul_line8_tilde_setup();
  matrix_mul_stat_tilde_setup();
  matrix_diag_mul_line_tilde_setup();
  matrix_diag_mul_line8_tilde_setup();
  matrix_diag_mul_stat_tilde_setup();
  matrix_bundle_line_tilde_setup();
  matrix_bundle_line8_tilde_setup();
  matrix_bundle_stat_tilde_setup();

  post("iem_ambi (1.21.1) library loaded!   (c) Thomas Musil "BUILD_DATE);
  post("   musil%ciem.at iem KUG Graz Austria", '@');
}
